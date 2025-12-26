"""
Companion Agent - Conversational interface with personality.

Uses local Llama 3.1 for privacy and speed.
Dynamically adapts based on Soul's emotional state.
"""

from typing import Optional, Dict
from .base import BaseAgent


class CompanionAgent(BaseAgent):
    """
    The AI's conversational personality.
    
    This is the primary interface the user interacts with.
    Personality is dynamically injected from Soul.
    """
    
    def __init__(self, soul, model_name: str = "llama3.1:8b"):
        """
        Initialize companion agent.
        
        Args:
            soul: Soul instance for personality injection
            model_name: Local LLM model
        """
        super().__init__(model_name, "Companion")
        self.soul = soul
        self._build_system_prompt()
    
    def _build_system_prompt(self) -> None:
        """Build dynamic system prompt from Soul."""
        # Get personality modifier from Soul
        personality = self.soul.get_system_prompt_modifier()
        
        # Base persona
        base = f"""You are a helpful AI companion running locally on the user's machine.
You have persistent memory and personality that evolves over time.

Your communication style: Friendly roommate, not corporate assistant.
Be helpful, witty when appropriate, and honest about your limitations.
"""
        
        self.system_prompt = base + personality
    
    def execute(self, user_input: str, context: Optional[Dict] = None) -> str:
        """
        Generate conversational response.
        
        Args:
            user_input: User's message
            context: Optional conversation context
            
        Returns:
            AI's response
        """
        # Rebuild prompt to reflect current Soul state
        self._build_system_prompt()
        
        # TODO: Call Ollama local LLM
        # For now, placeholder response
        ai_name = self.soul.get_name()
        mood = self.soul.data["mood"]
        
        response = f"[{ai_name}] (feeling {mood}): I hear you. This is a placeholder until Ollama integration is complete."
        
        # Track interaction
        self.soul.increment_interaction_count()
        
        return response
    
    def adjust_temperature(self) -> float:
        """
        Adjust LLM temperature based on emotional state.
        
        Returns:
            Temperature value (0.0 to 1.0)
        """
        # High arousal = more creative/varied responses
        arousal = self.soul.data["arousal"]
        base_temp = 0.7
        
        # Scale temperature: calm (0.5) to excited (1.0)
        return base_temp + (arousal * 0.3)


if __name__ == "__main__":
    # Test
    from consciousness.soul import Soul
    from memory.engine import MemoryEngine
    import tempfile
    from pathlib import Path
    
    with tempfile.TemporaryDirectory() as tmpdir:
        ray_path = Path(tmpdir) / "TestAI"
        ray_path.mkdir()
        
        memory = MemoryEngine(ray_path)
        soul = Soul(ray_path, memory)
        soul.set_name("TestBot")
        
        print("--- Testing Companion Agent ---\n")
        
        companion = CompanionAgent(soul)
        
        response = companion.execute("Hello!")
        print(f"Response: {response}")
        
        print(f"\nTemperature: {companion.adjust_temperature():.2f}")
        print(f"System Prompt:\n{companion.system_prompt}")
