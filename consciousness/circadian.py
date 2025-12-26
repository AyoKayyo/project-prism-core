"""
Circadian Rhythm - Idle Detection & Activity Monitoring

Cross-platform system activity monitoring.
"""

import time
from typing import Optional


class CircadianRhythm:
    """
    Monitors user activity patterns and idle time.
    Determines when to enter dream mode.
    """
    
    def __init__(self):
        """Initialize circadian rhythm monitor."""
        self.platform = self._detect_platform()
        self.last_activity_time = time.time()
    
    def _detect_platform(self) -> str:
        """Detect operating system."""
        import platform
        return platform.system()
    
    def get_idle_time(self) -> int:
        """
        Get seconds since last user input.
        
        Returns:
            Idle time in seconds
        """
        if self.platform == "Darwin":  # macOS
            return self._get_idle_macos()
        elif self.platform == "Windows":
            return self._get_idle_windows()
        elif self.platform == "Linux":
            return self._get_idle_linux()
        else:
            # Fallback: estimate based on last activity
            return int(time.time() - self.last_activity_time)
    
    def _get_idle_macos(self) -> int:
        """macOS idle detection using Quartz."""
        try:
            import Quartz
            return int(Quartz.CGEventSourceSecondsSinceLastEventType(
                Quartz.kCGEventSourceStateCombinedSessionState,
                Quartz.kCGAnyInputEventType
            ))
        except ImportError:
            # Quartz not available, use fallback
            return int(time.time() - self.last_activity_time)
    
    def _get_idle_windows(self) -> int:
        """Windows idle detection using ctypes."""
        try:
            import ctypes
            
            class LASTINPUTINFO(ctypes.Structure):
                _fields_ = [
                    ('cbSize', ctypes.c_uint),
                    ('dwTime', ctypes.c_ulong)
                ]
            
            lastInputInfo = LASTINPUTINFO()
            lastInputInfo.cbSize = ctypes.sizeof(lastInputInfo)
            ctypes.windll.user32.GetLastInputInfo(ctypes.byref(lastInputInfo))
            
            millis = ctypes.windll.kernel32.GetTickCount() - lastInputInfo.dwTime
            return int(millis / 1000)
        except Exception:
            return int(time.time() - self.last_activity_time)
    
    def _get_idle_linux(self) -> int:
        """Linux idle detection using xprintidle."""
        try:
            import subprocess
            idle_ms = subprocess.check_output(['xprintidle']).decode().strip()
            return int(idle_ms) // 1000
        except Exception:
            return int(time.time() - self.last_activity_time)
    
    def get_time_phase(self) -> str:
        """
        Get current time phase.
        
        Returns:
            "morning", "afternoon", "evening", or "night"
        """
        hour = time.localtime().tm_hour
        
        if 6 <= hour < 12:
            return "morning"
        elif 12 <= hour < 18:
            return "afternoon"
        elif 18 <= hour < 22:
            return "evening"
        else:
            return "night"
    
    def should_dream(self, idle_threshold: int = 300) -> bool:
        """
        Determine if should enter dream mode.
        
        Args:
            idle_threshold: Seconds of idle before dreaming (default: 300)
            
        Returns:
            True if should dream
        """
        return self.get_idle_time() >= idle_threshold
    
    def get_cpu_usage(self) -> float:
        """
        Get current CPU usage percentage.
        
        Returns:
            CPU usage (0.0 to 100.0)
        """
        try:
            import psutil
            return psutil.cpu_percent(interval=1)
        except ImportError:
            return 0.0
    
    def get_memory_usage(self) -> Dict:
        """
        Get memory usage statistics.
        
        Returns:
            Dictionary with memory info
        """
        try:
            import psutil
            mem = psutil.virtual_memory()
            return {
                "total_gb": mem.total / (1024**3),
                "used_gb": mem.used / (1024**3),
                "percent": mem.percent
            }
        except ImportError:
            return {"total_gb": 0, "used_gb": 0, "percent": 0}
    
    def calculate_fatigue(self, uptime_hours: float) -> float:
        """
        Calculate system fatigue based on uptime.
        
        Args:
            uptime_hours: Hours since AI started
            
        Returns:
            Fatigue level (0.0 = fresh, 1.0 = exhausted)
        """
        # Simple linear model: exhaust after 16 hours
        base_fatigue = min(1.0, uptime_hours / 16)
        
        # CPU usage also affects fatigue
        cpu = self.get_cpu_usage()
        stress_factor = (cpu / 100) * 0.2
        
        return min(1.0, base_fatigue + stress_factor)


if __name__ == "__main__":
    # Test
    print("--- Testing Circadian Rhythm ---\n")
    
    circadian = CircadianRhythm()
    
    print(f"Platform: {circadian.platform}")
    print(f"Idle time: {circadian.get_idle_time()}s")
    print(f"Time phase: {circadian.get_time_phase()}")
    print(f"Should dream: {circadian.should_dream(idle_threshold=5)}")
    print(f"CPU usage: {circadian.get_cpu_usage():.1f}%")
    print(f"Memory: {circadian.get_memory_usage()}")
    print(f"Fatigue (10h uptime): {circadian.calculate_fatigue(10):.2f}")
