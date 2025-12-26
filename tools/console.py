import time
import asyncio
from lab_senses import AdvancedSenses
from lab_memory import RileyMemory
from lab_subconscious import CuriosityEngine, Librarian, SelfReflection
from lab_soul import RileySoul
from lab_safety import SafetyCore
# Import calendar only if you have the credentials, otherwise use dummy
try:
    from lab_calendar import get_upcoming_events
except ImportError:
    def get_upcoming_events(): return "Calendar Module Offline"

class RileyConsciousness:
    def __init__(self):
        self.senses = AdvancedSenses()
        self.memory = RileyMemory()
        self.subconscious = CuriosityEngine(self.memory)
        self.librarian = Librarian(self.memory)
        self.reflection = SelfReflection(self.memory)
        self.soul = RileySoul(self.memory)
        self.safety = SafetyCore(self.soul)
        self.state = "BOOT"
        self.last_check = 0
        self.last_dream_time = 0

    def run_loop(self):
        print("⚡ [SYSTEM] Riley Nervous System Online")
        print("   - Monitoring Idle Time")
        print("   - Memory Core Active")
        
        while True:
            # 1. READ SENSES
            idle_time = self.senses.get_idle_time()
            phase = self.senses.get_time_phase()
            
            # 2. DECIDE STATE
            if idle_time > 10: # 5 Minutes Idle
                if self.state != "DREAMING":
                    print("💤 [State Change] User Away. Entering Dream Mode...")
                    self.memory.log_episode("NERVOUS_SYSTEM", "User went idle. Entering Dream Mode.")
                    self.state = "DREAMING"
            
            # 2.5 DREAM LOOP (If Dreaming)
            if self.state == "DREAMING" and (time.time() - self.last_dream_time > 10):
                # Every 10 seconds while dreaming, decide what to do
                import random
                dice = random.random()
                
                if dice < 0.3:
                    # 30% Chance to check for mess (Librarian)
                    if self.safety.track_usage("gemini-2.0-flash-lite", 500): # Est tokens
                        proposal = self.librarian.check_for_mess("test_messy_folder")
                        if proposal and "Proposed:" in proposal:
                            self.soul.grant_xp(5, "Librarian Proposal")

                elif dice < 0.5:
                     # 20% Chance to Reflect (30-50 range)
                     if self.safety.track_usage("gemini-2.0-flash-lite", 1000):
                         insight = self.reflection.reflect_on_day()
                         if insight:
                             self.soul.grant_xp(15, "Self-Reflection")

                else:
                    # 50% Chance to Ponder (Curiosity)
                    if self.safety.track_usage("gemini-2.0-flash-lite", 300):
                        thought = self.subconscious.ponder()
                        if thought:
                            self.soul.grant_xp(10, "Curiosity Epiphany")

                self.last_dream_time = time.time()
            
            elif idle_time < 5 and self.state == "DREAMING":
                print(f"☀️ [State Change] User Returned! Good {phase}.")
                self.memory.log_episode("NERVOUS_SYSTEM", f"User returned. Waking up. Phase: {phase}")
                self.state = "ACTIVE"
                self.trigger_morning_briefing()

            # 3. PULSE CHECK (Every 1 hour)
            if time.time() - self.last_check > 3600:
                self.run_hourly_maintenance()
                self.last_check = time.time()

            time.sleep(2) # Heartbeat

    def trigger_morning_briefing(self):
        """Called when you wake up the computer"""
        events = get_upcoming_events()
        # We don't print this, we would ideally inject it into the Chat UI
        # For now, we print to console to prove it works
        print(f"\n🔔 [NOTIFICATION] Welcome back, Mark.")
        print(f"   Here is your schedule:\n{events}\n")

    def run_hourly_maintenance(self):
        print("🧹 [MAINTENANCE] Organizing memories...")

if __name__ == "__main__":
    os = RileyConsciousness()
    os.run_loop()
