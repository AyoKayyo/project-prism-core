import time
import random
from PyQt6.QtCore import QThread, pyqtSignal

# Import your existing lab modules
from lab_senses import AdvancedSenses
from lab_memory import RileyMemory
from lab_subconscious import CuriosityEngine, Librarian, SelfReflection
from lab_soul import RileySoul
from lab_safety import SafetyCore

# Import calendar safely
try:
    from lab_calendar import get_upcoming_events
except ImportError:
    def get_upcoming_events(): 
        return "Calendar Module Offline"

class RileyConsciousness(QThread):
    """
    The Radio-Enabled Brain: Consciousness loop running as a background thread.
    Broadcasts pyqtSignals instead of using print() so the GUI can react.
    """
    # 📡 THE BROADCAST FREQUENCIES (Signals)
    signal_dream_start = pyqtSignal()         # Trigger: Dim Screen
    signal_dream_wake = pyqtSignal()          # Trigger: Undim Screen
    signal_morning_briefing = pyqtSignal(str) # Trigger: Post to Chat
    signal_log_update = pyqtSignal(str)       # Trigger: Update Status Bar

    def __init__(self):
        super().__init__()
        self.senses = AdvancedSenses()
        self.memory = RileyMemory()
        self.subconscious = CuriosityEngine(self.memory)
        self.librarian = Librarian(self.memory)
        self.reflection = SelfReflection(self.memory)
        self.soul = RileySoul(self.memory)
        self.safety = SafetyCore(self.soul)
        
        self.state = "BOOT"
        self.running = True
        self.last_check = 0
        self.last_dream_time = 0

    def run(self):
        """The Main Background Loop"""
        self.signal_log_update.emit("⚡ Nervous System Online")
        
        while self.running:
            # 1. READ SENSES
            idle_time = self.senses.get_idle_time()
            phase = self.senses.get_time_phase()
            
            # 2. STATE MACHINE
            # Check if dreaming is allowed
            if self.check_dream_conditions(idle_time, phase):
                if self.state != "DREAMING":
                    self.state = "DREAMING"
                    self.signal_dream_start.emit() # <--- FIRE SIGNAL
                    self.signal_log_update.emit("💤 Entering Dream Mode...")
            
                # DREAM LOOP
                if time.time() - self.last_dream_time > 10:
                    self.dream_cycle()
                    self.last_dream_time = time.time()
            
            elif idle_time < 5 and self.state == "DREAMING":
                self.state = "ACTIVE"
                self.signal_dream_wake.emit() # <--- FIRE SIGNAL
                self.signal_log_update.emit(f"☀️ Waking Up ({phase})")
                self.trigger_morning_briefing()

            # 3. MAINTENANCE (Hourly)
            if time.time() - self.last_check > 3600:
                self.run_hourly_maintenance()
                self.last_check = time.time()

            time.sleep(1) # Heartbeat

    def dream_cycle(self):
        """
        The Subconscious logic with error handling.
        During dreams, we prefer LOCAL LLM to save API costs.
        """
        dice = random.random()
        
        try:
            # Dream mode = LOCAL FIRST (user is away, save tokens!)
            llm_mode = "simple"  # Force local Ollama during dreams
            
            if dice < 0.3 and self.safety.track_usage("gemini-flash", 500):
                proposal = self.librarian.check_for_mess("test_messy_folder")
                if proposal: 
                    self.soul.grant_xp(5, "Librarian")
                    
            elif dice < 0.5 and self.safety.track_usage("gemini-flash", 1000):
                # Reflection can use local model for simple analysis
                insight = self.reflection.reflect_on_day()
                if insight: 
                    self.soul.grant_xp(15, "Reflection")

            else:
                # Curiosity during dreams = local LLM (free!)
                if self.safety.track_usage("local-llm", 0):  # Zero cost for local
                    thought = self.subconscious.ponder(mode="simple")  # Force local
                    if thought: 
                        self.soul.grant_xp(10, "Curiosity")
        except Exception as e:
            # Log API errors but don't crash
            self.signal_log_update.emit(f"⚠️ Dream interrupted: {str(e)[:50]}")

    def check_dream_conditions(self, idle_time, phase):
        """
        Smart dream trigger logic - checks multiple conditions.
        
        Returns True if Riley should enter dream mode.
        """
        # 1. Idle time check (TEST: 10s, PRODUCTION: 300s)
        if idle_time < 10:
            return False
        
        # 2. CPU usage check (don't dream during high load)
        try:
            cpu_usage = self.senses.get_cpu_usage()
            if cpu_usage > 60:
                return False
        except AttributeError:
            pass  # Sensor doesn't support CPU check
        
        # 3. Active window blocklist
        try:
            active_window = self.senses.get_active_window()
            blocklist = ["Code", "VSCode", "Visual Studio", "Game", "Steam", "Epic"]
            if any(blocked in active_window for blocked in blocklist):
                return False
        except AttributeError:
            pass  # Sensor doesn't support window detection
        
        return True

    def trigger_morning_briefing(self):
        """Generate morning briefing when waking up"""
        events = get_upcoming_events()
        msg = f"**Welcome back.**\n\n📅 **Schedule:**\n{events}"
        self.signal_morning_briefing.emit(msg)

    def run_hourly_maintenance(self):
        """Periodic maintenance tasks"""
        self.signal_log_update.emit("🧹 Maintenance Cycle")
        
    def stop(self):
        """Gracefully stop the consciousness loop"""
        self.running = False
        self.wait()
