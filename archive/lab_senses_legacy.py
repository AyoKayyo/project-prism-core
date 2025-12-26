import Quartz
import psutil
import time
from datetime import datetime
from AppKit import NSWorkspace

class AdvancedSenses:
    def get_idle_time(self):
        """Eyes: How long has the user been gone?"""
        return Quartz.CGEventSourceSecondsSinceLastEventType(
            Quartz.kCGEventSourceStateCombinedSessionState, 
            Quartz.kCGAnyInputEventType
        )

    def get_battery_status(self):
        """Energy: Are we dying?"""
        batt = psutil.sensors_battery()
        if batt:
            return {
                "percent": round(batt.percent, 1),
                "plugged": batt.power_plugged,
                "status": "Charging" if batt.power_plugged else "Draining"
            }
        return {"percent": 100, "plugged": True, "status": "Desktop Mode"}

    def get_active_app(self):
        """Context: What is Mark working on?"""
        app = NSWorkspace.sharedWorkspace().frontmostApplication()
        if app:
            return app.localizedName()
        return "Unknown"

    def get_time_phase(self):
        """Circadian Rhythm"""
        h = datetime.now().hour
        if 5 <= h < 12: return "MORNING"
        if 12 <= h < 18: return "WORK_BLOCK"
        if 18 <= h < 23: return "EVENING"
        return "DEEP_NIGHT"

    def full_scan(self):
        print("\n👁️ [SENSORY INPUT SCAN]")
        print(f"   - Phase:    {self.get_time_phase()}")
        print(f"   - App:      {self.get_active_app()}")
        print(f"   - Battery:  {self.get_battery_status()}")
        print(f"   - Idle:     {self.get_idle_time():.1f} sec")

if __name__ == "__main__":
    senses = AdvancedSenses()
    while True:
        senses.full_scan()
        time.sleep(3)
