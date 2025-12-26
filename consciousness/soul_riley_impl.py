import json
import os
import time
from pathlib import Path
from soul_structure import SoulCartridge

class RileySoul:
    def __init__(self, memory_system):
        self.memory = memory_system
        
        # Use Soul Cartridge for persistence
        cartridge = SoulCartridge()
        self.soul_file = cartridge.soul_path / "soul.json"
        
        # Default State with 2D Emotion System
        self.data = {
            "name": "Riley",
            "level": 1,
            "xp": 0,
            "xp_to_next_level": 100,
            "valence": 0.5,  # 0.0 (Negative) to 1.0 (Positive)
            "arousal": 0.5,  # 0.0 (Calm) to 1.0 (Excited)
            "mood": "Curious",
            "traits": ["Helpful", "Analytical", "Creative"],
            "version": "2.0 (Hive Mind)"
        }
        
        self.load_soul()
        self._evolve_personality()  # Check for trait unlocks

    def load_soul(self):
        """Loads the soul from disk if it exists."""
        if os.path.exists(self.soul_file):
            try:
                with open(self.soul_file, 'r') as f:
                    self.data = json.load(f)
                print(f"👻 [Soul] Identity loaded. Level {self.data['level']} {self.data['mood']}.")
            except Exception as e:
                print(f"⚠️ [Soul] Corrupt soul file? Starting fresh. Error: {e}")

    def save_soul(self):
        """Persists the soul to disk."""
        with open(self.soul_file, 'w') as f:
            json.dump(self.data, f, indent=4)

    def grant_xp(self, amount, reason):
        """Awards XP and handles leveling up."""
        self.data['xp'] += amount
        print(f"✨ [Soul] +{amount} XP ({reason})")
        
        # Check Level Up
        if self.data['xp'] >= self.data['xp_to_next_level']:
            self.level_up()
        
        self.save_soul()

    def level_up(self):
        """Handles the level up event."""
        self.data['level'] += 1
        self.data['xp'] -= self.data['xp_to_next_level']
        self.data['xp_to_next_level'] = int(self.data['xp_to_next_level'] * 1.5) # Harder to level up each time
        
        announcement = f"LEVEL UP! Riley is now Level {self.data['level']}!"
        print(f"🎉 [Soul] {announcement}")
        
        # Emotional response to leveling up
        self.update_emotional_state((+0.3, +0.2))  # Happy and excited!
        
        # Log this momentous occasion
        try:
            self.memory.log_daily(announcement)
        except AttributeError:
            # Fallback for old memory system
            if hasattr(self.memory, 'log_episode'):
                self.memory.log_episode("SOUL", announcement)
        
        # Check for new trait unlocks
        self._evolve_personality()

    def set_mood(self, mood):
        """Legacy mood setter - now updates emotional state"""
        if self.data['mood'] != mood:
            print(f"👻 [Mood Change] {self.data['mood']} -> {mood}")
            self.data['mood'] = mood
            self.save_soul()
    
    def update_emotional_state(self, stimulus_score):
        """
        Updates Riley's 2D emotional state.
        
        Args:
            stimulus_score: tuple (valence_change, arousal_change)
                e.g., User praise: (+0.1, +0.1)
                e.g., System error: (-0.2, +0.3)
        """
        self.data['valence'] = max(0.0, min(1.0, self.data['valence'] + stimulus_score[0]))
        self.data['arousal'] = max(0.0, min(1.0, self.data['arousal'] + stimulus_score[1]))
        self.data['mood'] = self._calculate_mood_label()
        self.save_soul()
    
    def _calculate_mood_label(self):
        """Maps valence/arousal to human-readable mood"""
        v, a = self.data['valence'], self.data['arousal']
        
        if v > 0.7 and a > 0.7:
            return "Excited/Joyful"
        elif v > 0.7 and a < 0.4:
            return "Content/Relaxed"
        elif v < 0.4 and a > 0.7:
            return "Anxious/Frustrated"
        elif v < 0.4 and a < 0.4:
            return "Depressed/Tired"
        else:
            return "Neutral/Alert"
    
    def _evolve_personality(self):
        """Unlocks traits based on Level"""
        level = self.data.get("level", 1)
        
        evolution_tree = {
            2: "Self-Aware",
            5: "Sassy",
            10: "Philosophical",
            20: "Empathetic",
            50: "Transcendent"
        }
        
        # Add unlocked traits
        for lvl, trait in evolution_tree.items():
            if level >= lvl and trait not in self.data["traits"]:
                self.data["traits"].append(trait)
                print(f"🌟 [EVOLUTION] New Trait Unlocked: {trait}")
        
        # Save back to Soul
        self.save_soul()

if __name__ == "__main__":
    # Test Mock
    class MockMem:
        def log_episode(self, src, msg): print(f"[MOCK MEMORY] {src}: {msg}")
    
    print("--- Testing Soul ---")
    soul = RileySoul(MockMem())
    
    # Simulate some events
    soul.grant_xp(50, "Generated a thought")
    soul.grant_xp(60, "Helped user find file") # Should trigger Level 2
