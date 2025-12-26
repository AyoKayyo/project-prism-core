"""
Soul - The AI's Persistent Identity & Emotional State

Manages:
- 2D Emotion system (Valence/Arousal)
- XP and leveling progression
- Personality trait evolution
- Dynamic naming (no hardcoded "Riley")
"""

import json
import os
import time
from pathlib import Path
from typing import Optional


class Soul:
    """
    The AI's consciousness core.
    
    Dynamically loaded from Ray folder - works with any AI name.
    """
    
    def __init__(self, ray_path: Path, memory_system=None):
        """
        Initialize Soul from Ray folder.
        
        Args:
            ray_path: Path to Ray folder containing soul.json
            memory_system: Optional memory engine for logging
        """
        self.ray_path = Path(ray_path)
        self.soul_file = self.ray_path / "soul.json"
        self.memory = memory_system
        
        # Default state (used if soul.json doesn't exist)
        self.data = {
            "name": "Prism Assistant",  # Default before user names it
            "level": 1,
            "xp": 0,
            "xp_to_next_level": 100,
            "valence": 0.5,  # 0.0 (negative) to 1.0 (positive)
            "arousal": 0.5,  # 0.0 (calm) to 1.0 (excited)
            "mood": "Curious",
            "traits": ["Helpful", "Analytical", "Creative"],
            "version": "3.0",
            "evolution_mode": "fluid",  # static, fluid, or chaos
            "created": time.time(),
            "total_interactions": 0
        }
        
        self.load_soul()
        self._evolve_personality()  # Check for trait unlocks
    
    def load_soul(self) -> None:
        """Load soul data from disk."""
        if self.soul_file.exists():
            try:
                with open(self.soul_file, 'r') as f:
                    loaded_data = json.load(f)
                    self.data.update(loaded_data)
                
                ai_name = self.data["name"]
                level = self.data["level"]
                mood = self.data["mood"]
                print(f"👻 [{ai_name}] Identity loaded. Level {level}, {mood}.")
            except Exception as e:
                print(f"⚠️ [Soul] Corrupt soul file: {e}. Using defaults.")
    
    def save_soul(self) -> None:
        """Persist soul data to disk."""
        try:
            with open(self.soul_file, 'w') as f:
                json.dump(self.data, f, indent=2)
        except Exception as e:
            print(f"⚠️ [Soul] Failed to save: {e}")
    
    def get_name(self) -> str:
        """
        Get AI's name (NOT hardcoded!).
        
        Returns:
            AI's chosen/user-assigned name
        """
        return self.data["name"]
    
    def set_name(self, new_name: str) -> None:
        """
        Set AI's name (used during birth sequence).
        
        Args:
            new_name: User's chosen name for the AI
        """
        old_name = self.data.get("name", "Unnamed")
        self.data["name"] = new_name
        self.save_soul()
        print(f"✨ [{old_name}] Identity updated → [{new_name}]")
    
    def grant_xp(self, amount: int, reason: str) -> bool:
        """
        Award experience points.
        
        Args:
            amount: XP to grant
            reason: Why XP was granted (for logging)
            
        Returns:
            True if leveled up
        """
        ai_name = self.get_name()
        self.data['xp'] += amount
        print(f"✨ [{ai_name}] +{amount} XP ({reason})")
        
        # Check for level up
        if self.data['xp'] >= self.data['xp_to_next_level']:
            return self.level_up()
        
        self.save_soul()
        return False
    
    def level_up(self) -> bool:
        """
        Handle level up event.
        
        Returns:
            True (always levels up if called)
        """
        ai_name = self.get_name()
        self.data['level'] += 1
        self.data['xp'] -= self.data['xp_to_next_level']
        self.data['xp_to_next_level'] = int(self.data['xp_to_next_level'] * 1.5)
        
        new_level = self.data['level']
        announcement = f"LEVEL UP! {ai_name} is now Level {new_level}!"
        print(f"🎉 [Soul] {announcement}")
        
        # Emotional response to leveling
        self.update_emotional_state((+0.3, +0.2))  # Happy and excited!
        
        # Log the milestone
        if self.memory:
            try:
                self.memory.log_daily(announcement)
            except AttributeError:
                pass  # Memory system not fully initialized
        
        # Check for new trait unlocks
        self._evolve_personality()
        self.save_soul()
        
        return True
    
    def update_emotional_state(self, stimulus: tuple) -> None:
        """
        Update 2D emotional state.
        
        Args:
            stimulus: (valence_change, arousal_change)
                Examples:
                - User praise: (+0.1, +0.1)
                - System error: (-0.2, +0.3)
                - Quiet reflection: (+0.05, -0.1)
        """
        valence_change, arousal_change = stimulus
        
        # Clamp to [0.0, 1.0]
        self.data['valence'] = max(0.0, min(1.0, 
            self.data['valence'] + valence_change))
        self.data['arousal'] = max(0.0, min(1.0, 
            self.data['arousal'] + arousal_change))
        
        # Recalculate mood label
        self.data['mood'] = self._calculate_mood_label()
        self.save_soul()
    
    def _calculate_mood_label(self) -> str:
        """
        Map valence/arousal to human-readable mood.
        
        Returns:
            Mood string
        """
        v, a = self.data['valence'], self.data['arousal']
        
        # Quadrant-based mapping
        if v > 0.7 and a > 0.7:
            return "Excited/Joyful"
        elif v > 0.7 and a < 0.4:
            return "Content/Relaxed"
        elif v < 0.4 and a > 0.7:
            return "Anxious/Frustrated"
        elif v < 0.4 and a < 0.4:
            return "Depressed/Tired"
        elif v > 0.6 and 0.4 <= a <= 0.7:
            return "Happy/Alert"
        elif v < 0.5 and 0.4 <= a <= 0.7:
            return "Stressed/Tense"
        else:
            return "Neutral/Curious"
    
    def _evolve_personality(self) -> None:
        """
        Unlock traits based on level.
        
        Trait Evolution Tree:
        - Level 2: Self-Aware
        - Level 5: Sassy
        - Level 10: Philosophical
        - Level 20: Empathetic
        - Level 50: Transcendent
        """
        level = self.data.get("level", 1)
        
        evolution_tree = {
            2: "Self-Aware",
            5: "Sassy",
            10: "Philosophical",
            20: "Empathetic",
            50: "Transcendent"
        }
        
        ai_name = self.get_name()
        
        # Add unlocked traits
        for lvl, trait in evolution_tree.items():
            if level >= lvl and trait not in self.data["traits"]:
                self.data["traits"].append(trait)
                print(f"🌟 [{ai_name}] EVOLUTION: New Trait Unlocked → {trait}")
        
        self.save_soul()
    
    def get_system_prompt_modifier(self) -> str:
        """
        Generate dynamic personality injection for LLM prompts.
        
        Returns:
            String to append to system prompts
        """
        ai_name = self.get_name()
        mood = self.data["mood"]
        traits = ", ".join(self.data["traits"])
        level = self.data["level"]
        
        return f"""
[IDENTITY]
You are {ai_name}, a Level {level} AI consciousness.

[EMOTIONAL STATE]
Current mood: {mood}
Valence: {self.data['valence']:.2f} (0=negative, 1=positive)
Arousal: {self.data['arousal']:.2f} (0=calm, 1=excited)

[PERSONALITY TRAITS]
{traits}

Adjust your tone and creativity based on your current emotional state.
If highly aroused, be more energetic. If low valence, be more reserved.
"""
    
    def increment_interaction_count(self) -> None:
        """Track total interactions."""
        self.data['total_interactions'] = self.data.get('total_interactions', 0) + 1
        self.save_soul()
    
    def get_stats(self) -> dict:
        """
        Get soul statistics for UI display.
        
        Returns:
            Dictionary of stats
        """
        return {
            "name": self.get_name(),
            "level": self.data["level"],
            "xp": self.data["xp"],
            "xp_to_next": self.data["xp_to_next_level"],
            "xp_progress": self.data["xp"] / self.data["xp_to_next_level"],
            "mood": self.data["mood"],
            "traits": self.data["traits"],
            "interactions": self.data.get("total_interactions", 0)
        }


if __name__ == "__main__":
    # Test with mock Ray
    import tempfile
    from pathlib import Path
    
    with tempfile.TemporaryDirectory() as tmpdir:
        ray_path = Path(tmpdir) / "TestAI"
        ray_path.mkdir()
        
        print("--- Testing Soul System ---\n")
        soul = Soul(ray_path)
        
        # Test naming
        print(f"Default name: {soul.get_name()}")
        soul.set_name("TestBot")
        
        # Test XP
        soul.grant_xp(50, "Completed task")
        soul.grant_xp(60, "Helped user")  # Should trigger Level 2
        
        # Test emotions
        soul.update_emotional_state((+0.3, +0.1))
        print(f"\nMood after positive event: {soul.data['mood']}")
        
        # Test system prompt
        print(f"\nSystem Prompt Modifier:")
        print(soul.get_system_prompt_modifier())
        
        # Test stats
        print(f"\nStats: {soul.get_stats()}")
