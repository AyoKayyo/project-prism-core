"""
Hardware Abstraction Layer (HAL) - Riley v2.0
Cross-platform sensor system for macOS, Windows, and Linux
"""
import platform
import os
import subprocess
import time
import psutil
from datetime import datetime

class HardwareAbstractionLayer:
    """
    Cross-platform sensor system that abstracts hardware differences
    between macOS, Windows, and Linux.
    """
    
    def __init__(self):
        self.system = platform.system()
        self.soul_path = os.getenv("RILEY_SOUL_PATH")
        
        # Platform-specific imports
        if self.system == "Windows":
            try:
                import win32gui
                import win32process
                self.win32gui = win32gui
                self.win32process = win32process
            except ImportError:
                print("⚠️  [HAL] pywin32 not installed. Windows features limited.")
                self.win32gui = None
                self.win32process = None
        
        print(f"🖥️  [HAL] Initialized on {self.system}")
    
    def get_idle_time(self):
        """
        Returns idle time in seconds (time since last user input).
        Cross-platform implementation.
        """
        try:
            if self.system == "Darwin":  # macOS
                # Use ioreg to get HID idle time
                cmd = "ioreg -c IOHIDSystem | awk '/HIDIdleTime/ {print $NF/1000000000; exit}'"
                result = subprocess.check_output(cmd, shell=True).decode().strip()
                return int(float(result))
            
            elif self.system == "Windows":
                # Use GetLastInputInfo from win32api
                try:
                    import ctypes
                    class LASTINPUTINFO(ctypes.Structure):
                        _fields_ = [("cbSize", ctypes.c_uint), ("dwTime", ctypes.c_uint)]
                    
                    lii = LASTINPUTINFO()
                    lii.cbSize = ctypes.sizeof(LASTINPUTINFO)
                    ctypes.windll.user32.GetLastInputInfo(ctypes.byref(lii))
                    millis = ctypes.windll.kernel32.GetTickCount() - lii.dwTime
                    return millis / 1000.0
                except Exception as e:
                    print(f"⚠️  [HAL] Windows idle detection error: {e}")
                    return 0
            
            elif self.system == "Linux":
                # Use xprintidle
                try:
                    result = subprocess.check_output(["xprintidle"]).decode().strip()
                    return int(result) / 1000.0
                except FileNotFoundError:
                    print("⚠️  [HAL] xprintidle not installed. Install with: sudo apt install xprintidle")
                    return 0
            
            else:
                return 0
                
        except Exception as e:
            print(f"⚠️  [HAL] Idle time error: {e}")
            return 0
    
    def get_time_phase(self):
        """Returns current time phase: Morning, Afternoon, Evening, or Night"""
        hour = datetime.now().hour
        
        if 5 <= hour < 12:
            return "Morning"
        elif 12 <= hour < 17:
            return "Afternoon"
        elif 17 <= hour < 21:
            return "Evening"
        else:
            return "Night"
    
    def get_cpu_usage(self):
        """Returns current CPU usage percentage"""
        return psutil.cpu_percent(interval=1)
    
    def get_memory_usage(self):
        """Returns current memory usage percentage"""
        return psutil.virtual_memory().percent
    
    def get_battery_status(self):
        """
        Returns battery information as dict.
        Returns None if no battery (desktop).
        """
        battery = psutil.sensors_battery()
        if battery is None:
            return None
        
        return {
            "percent": battery.percent,
            "plugged_in": battery.power_plugged,
            "time_left": battery.secsleft if battery.secsleft != psutil.POWER_TIME_UNLIMITED else None
        }
    
    def get_active_window(self):
        """
        Returns the title of the currently active window.
        Platform-specific implementation.
        """
        try:
            if self.system == "Darwin":  # macOS
                script = '''
                tell application "System Events"
                    set frontApp to name of first application process whose frontmost is true
                end tell
                return frontApp
                '''
                result = subprocess.check_output(["osascript", "-e", script]).decode().strip()
                return result
            
            elif self.system == "Windows":
                if self.win32gui:
                    window = self.win32gui.GetForegroundWindow()
                    return self.win32gui.GetWindowText(window)
                return "Unknown"
            
            elif self.system == "Linux":
                # Try wmctrl
                try:
                    result = subprocess.check_output(["xdotool", "getactivewindow", "getwindowname"]).decode().strip()
                    return result
                except FileNotFoundError:
                    return "Unknown"
            
            else:
                return "Unknown"
                
        except Exception as e:
            return f"Error: {e}"
    
    def scan_environment(self):
        """
        Comprehensive environment scan.
        Returns dictionary of all sensor readings.
        """
        return {
            "timestamp": time.time(),
            "idle_time": self.get_idle_time(),
            "time_phase": self.get_time_phase(),
            "cpu_usage": self.get_cpu_usage(),
            "memory_usage": self.get_memory_usage(),
            "battery": self.get_battery_status(),
            "active_window": self.get_active_window(),
            "platform": self.system
        }
    
    def is_user_active(self):
        """
        Returns True if user is currently active (not idle).
        """
        return self.get_idle_time() < 60  # Active if input within last minute
    
    def is_high_load(self):
        """
        Returns True if system is under high load (gaming, rendering, etc.)
        """
        return self.get_cpu_usage() > 60


# Backward compatibility - create alias to old name
AdvancedSenses = HardwareAbstractionLayer


if __name__ == "__main__":
    # Test HAL
    print("🧪 Testing Hardware Abstraction Layer\n")
    
    hal = HardwareAbstractionLayer()
    
    print("📊 Environment Scan:")
    stats = hal.scan_environment()
    for key, value in stats.items():
        if key == "battery" and value:
            print(f"  {key}:")
            for k, v in value.items():
                print(f"    {k}: {v}")
        else:
            print(f"  {key}: {value}")
    
    print(f"\n✅ User Active: {hal.is_user_active()}")
    print(f"⚡ High Load: {hal.is_high_load()}")
