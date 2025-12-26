"""
Cross-platform Notification System - Riley v2.0
Sends system notifications and plays alert sounds
"""
import platform
import os
import subprocess


def notify(title, message):
    """
    Sends a system notification with sound.
    Cross-platform: macOS, Windows, Linux
    
    Args:
        title: Notification title
        message: Notification body text
    """
    system = platform.system()
    
    try:
        if system == "Darwin":  # macOS
            # Use osascript for notification
            script = f'display notification "{message}" with title "{title}"'
            subprocess.run(["osascript", "-e", script], check=True)
            
            # Play system sound
            subprocess.run(["afplay", "/System/Library/Sounds/Glass.aiff"])
            
        elif system == "Windows":
            # Use win10toast
            try:
                from win10toast import ToastNotifier
                toaster = ToastNotifier()
                toaster.show_toast(title, message, duration=5, threaded=True)
            except ImportError:
                print("⚠️ win10toast not installed. Install with: pip install win10toast")
                
        elif system == "Linux":
            # Use notify-send
            try:
                subprocess.run(["notify-send", title, message], check=True)
                # Try to play sound
                subprocess.run(["paplay", "/usr/share/sounds/freedesktop/stereo/message.oga"], 
                             stderr=subprocess.DEVNULL)
            except FileNotFoundError:
                print("⚠️ notify-send not found. Install with: sudo apt install libnotify-bin")
        
        print(f"🔔 [Notify] {title}: {message}")
        return True
        
    except Exception as e:
        print(f"⚠️ [Notify] Failed: {e}")
        return False


if __name__ == "__main__":
    # Test notifications
    print("🧪 Testing Notification System\n")
    
    notify("Riley Consciousness", "Visual Cortex test complete!")
    notify("Riley", "I've learned something new")
