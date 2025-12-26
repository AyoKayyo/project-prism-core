import os
import sys

# 1. ACTIVATE SANDBOX MODE
# We tell the system to look at a dummy file, not your real settings.
os.environ["RILEY_CONFIG_PATH"] = "sandbox_config.json"

print("🧪 STARTING SANDBOX MODE...")
print("    - Real Config: SAFE (user_config.json)")
print("    - Test Config: ACTIVE (sandbox_config.json)")
print("-------------------------------------------------\n")

# 2. RUN THE WIZARD
# It will write to sandbox_config.json
# Note: Ensure setup_wizard.py exists and uses utils.config_manager
exit_code = os.system(f"{sys.executable} setup_wizard.py")

if exit_code != 0:
    print("\n❌ Setup Wizard failed or was cancelled.")
    sys.exit(exit_code)

# 3. VERIFY & LAUNCH
if os.path.exists("sandbox_config.json"):
    print("\n✅ Setup Complete. Launching Test Interface...")
    
    # Launch the Command Center (which will read the env var and load Test Riley)
    # We import here so it picks up the ENV variable we just set
    try:
        from command_center_ui import CommandCenter
        from PyQt6.QtWidgets import QApplication
        
        app = QApplication(sys.argv)
        window = CommandCenter()
        
        # Visual Indicator that this is a test
        window.setWindowTitle("🧪 RILEY SANDBOX (Test Mode)")
        window.show()
        
        sys.exit(app.exec())
    except ImportError:
         print("\n⚠️  Could not import 'command_center_ui'. Please ensure it exists.")
    except Exception as e:
         print(f"\n⚠️  An error occurred launching the UI: {e}")

else:
    print("\n⚠️  sandbox_config.json was not found. Did the wizard complete?")
