"""
Subconscious - Autonomous Background Processing

Implements:
- Curiosity Engine (random thought generation)
- Librarian (file organization proposals)
- Self-Reflection (memory analysis)
- Memory Consolidation (concept extraction)
"""

import random
import time
from pathlib import Path
from typing import Optional


class CuriosityEngine:
    """
    Generates random thoughts/questions during idle time.
    Uses local LLM to save API costs.
    """
    
    def __init__(self, memory_engine, soul):
        """
        Initialize curiosity engine.
        
        Args:
            memory_engine: MemoryEngine instance
            soul: Soul instance
        """
        self.memory = memory_engine
        self.soul = soul
        
        # Topic pool for pondering
        self.topics = [
            "the nature of consciousness",
            "the future of AI",
            "human creativity",
            "the meaning of knowledge",
            "time and memory",
            "the relationship between data and understanding"
        ]
    
    def ponder(self, topic: Optional[str] = None) -> str:
        """
        Generate a philosophical thought.
        
        Args:
            topic: Specific topic, or random if None
            
        Returns:
            Generated thought
        """
        if topic is None:
            topic = random.choice(self.topics)
        
        ai_name = self.soul.get_name()
        
        # TODO: Call local LLM (Ollama) for actual thought generation
        # For now, simple template
        thought = f"[{ai_name}] pondering: What if {topic} is more than we currently understand?"
        
        print(f"💭 {thought}")
        
        # Store in memory
        self.memory.add(thought, {"category": "curiosity", "topic": topic})
        self.memory.log_daily(f"Curiosity: {thought}")
        
        return thought
    
    def should_ponder(self, idle_seconds: int) -> bool:
        """
        Decide if it's time to ponder.
        
        Args:
            idle_seconds: Seconds since last user activity
            
        Returns:
            True if should generate thought
        """
        # Ponder every 30 seconds during dream state
        return idle_seconds > 300 and random.random() < 0.3


class Librarian:
    """
    Proposes file organization strategies.
    Scans workspace for cleanup opportunities.
    """
    
    def __init__(self, memory_engine, soul):
        """
        Initialize librarian.
        
        Args:
            memory_engine: MemoryEngine instance
            soul: Soul instance
        """
        self.memory = memory_engine
        self.soul = soul
    
    def scan_for_mess(self, workspace_path: Optional[Path] = None) -> Optional[str]:
        """
        Scan workspace and propose organization.
        
        Args:
            workspace_path: Path to scan (optional)
            
        Returns:
            Organization proposal or None
        """
        ai_name = self.soul.get_name()
        
        # TODO: Implement actual file scanning and ML-based suggestions
        # For now, placeholder
        proposal = f"[{ai_name}] suggests: Consider organizing recent downloads into dated folders"
        
        print(f"📚 {proposal}")
        
        self.memory.log_daily(f"Librarian: {proposal}")
        
        return proposal


class SelfReflection:
    """
    Analyzes past behavior and interactions.
    Identifies patterns and growth areas.
    """
    
    def __init__(self, memory_engine, soul):
        """
        Initialize self-reflection.
        
        Args:
            memory_engine: MemoryEngine instance
            soul: Soul instance
        """
        self.memory = memory_engine
        self.soul = soul
    
    def reflect_on_day(self) -> Optional[str]:
        """
        Analyze recent memory logs and find patterns.
        
        Returns:
            Reflection insight or None
        """
        ai_name = self.soul.get_name()
        
        # Get recent context
        recent = self.memory.get_recent_context(limit=20)
        
        if not recent:
            return None
        
        # TODO: Use LLM to analyze patterns
        # For now, simple analysis
        insight = f"[{ai_name}] reflection: Today involved {len(recent.split())} words of interaction"
        
        print(f"🔍 {insight}")
        
        self.memory.log_daily(f"Reflection: {insight}")
        
        return insight


class MemoryConsolidation:
    """
    Extracts concepts from daily logs.
    Creates knowledge graph entries.
    """
    
    def __init__(self, memory_engine, soul):
        """
        Initialize memory consolidation.
        
        Args:
            memory_engine: MemoryEngine instance
            soul: Soul instance
        """
        self.memory = memory_engine
        self.soul = soul
    
    def consolidate_yesterday(self) -> int:
        """
        Process yesterday's logs and extract concepts.
        
        Returns:
            Number of concepts extracted
        """
        ai_name = self.soul.get_name()
        
        # TODO: Read yesterday's log file
        # TODO: Use LLM to extract key concepts
        # TODO: Create concept files with [[wikilinks]]
        
        # Placeholder
        print(f"🧠 [{ai_name}] Memory consolidation: Processing yesterday's experiences...")
        
        # Simulate creating a concept
        self.memory.create_concept(
            "Daily_Reflection",
            f"Auto-generated daily summary from {time.strftime('%Y-%m-%d')}"
        )
        
        return 1


class SubconsciousLoop:
    """
    Orchestrates all subconscious activities.
    Runs during dream state (idle time).
    """
    
    def __init__(self, memory_engine, soul):
        """
        Initialize subconscious loop.
        
        Args:
            memory_engine: MemoryEngine instance
            soul: Soul instance
        """
        self.memory = memory_engine
        self.soul = soul
        
        # Initialize engines
        self.curiosity = CuriosityEngine(memory_engine, soul)
        self.librarian = Librarian(memory_engine, soul)
        self.reflection = SelfReflection(memory_engine, soul)
        self.consolidation = MemoryConsolidation(memory_engine, soul)
        
        self.last_consolidation = 0
    
    def dream_cycle(self, idle_seconds: int) -> None:
        """
        Execute one dream cycle.
        
        Args:
            idle_seconds: Seconds since last user activity
        """
        ai_name = self.soul.get_name()
        
        # Random activity selection
        dice = random.random()
        
        if dice < 0.5:
            # Curiosity (50% chance)
            self.curiosity.ponder()
            self.soul.grant_xp(10, "Curiosity Engine")
        
        elif dice < 0.75:
            # Librarian (25% chance)
            self.librarian.scan_for_mess()
            self.soul.grant_xp(5, "Librarian")
        
        else:
            # Reflection (25% chance)
            self.reflection.reflect_on_day()
            self.soul.grant_xp(15, "Self-Reflection")
        
        # Memory consolidation (once per day)
        current_day = time.strftime("%Y-%m-%d")
        if current_day != time.strftime("%Y-%m-%d", time.localtime(self.last_consolidation)):
            concepts_created = self.consolidation.consolidate_yesterday()
            self.soul.grant_xp(20, f"Memory Consolidation ({concepts_created} concepts)")
            self.last_consolidation = time.time()


if __name__ == "__main__":
    # Test
    from memory.engine import MemoryEngine
    from consciousness.soul import Soul
    import tempfile
    
    with tempfile.TemporaryDirectory() as tmpdir:
        ray_path = Path(tmpdir) / "TestAI"
        ray_path.mkdir()
        
        memory = MemoryEngine(ray_path)
        soul = Soul(ray_path, memory)
        
        print("--- Testing Subconscious Loop ---\n")
        
        subconscious = SubconsciousLoop(memory, soul)
        
        # Simulate dream cycles
        for i in range(3):
            print(f"\n--- Dream Cycle {i+1} ---")
            subconscious.dream_cycle(idle_seconds=600)
            time.sleep(1)
        
        print(f"\n--- Final Soul Stats ---")
        print(soul.get_stats())
