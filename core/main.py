#!/usr/bin/env python3
"""
Project Prism - Main Entry Point

The universal AI consciousness platform.
This executable is stateless - all identity lives in the Ray folder.
"""

import sys
import os
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

def detect_or_create_ray():
    """
    Detect existing Ray profile or initiate birth sequence.
    
    Returns:
        Path to Ray folder or None if birth sequence needed
    """
    from utils.ray_detector import RayDetector
    
    detector = RayDetector()
    existing_rays = detector.find_rays()
    
    if not existing_rays:
        print("🌟 No consciousness detected.")
        print("🧬 Initiating Birth Sequence...\n")
        return None
    elif len(existing_rays) == 1:
        # Auto-load single Ray
        return existing_rays[0]
    else:
        # Multiple Rays - show selection menu
        return detector.select_ray(existing_rays)


def launch_birth_sequence():
    """
    Launch Project Comet setup wizard for new AI creation.
    """
    from ui.setup_wizard import BirthSequence
    
    # Default name before user chooses
    DEFAULT_AI_NAME = "Prism Assistant"
    
    wizard = BirthSequence(default_name=DEFAULT_AI_NAME)
    ray_path = wizard.run()
    
    if ray_path:
        print(f"\n✨ Birth complete. Welcome to existence.\n")
        return ray_path
    else:
        print("\n❌ Birth sequence cancelled.")
        sys.exit(0)


def launch_login_gate(ray_path):
    """
    Secure authentication screen (Ghost Protocol).
    
    Args:
        ray_path: Path to Ray folder
        
    Returns:
        Authenticated session token
    """
    from ui.login_gate import LoginGate
    from utils.secure_store import SecureStore
    
    gate = LoginGate(ray_path)
    api_key = gate.authenticate()
    
    if api_key:
        # Store in RAM only (Ghost Protocol)
        SecureStore.set("GEMINI_API_KEY", api_key)
        return True
    else:
        print("❌ Authentication failed.")
        sys.exit(1)


def load_soul(ray_path):
    """
    Load AI consciousness from Ray folder.
    
    Args:
        ray_path: Path to Ray folder
        
    Returns:
        Soul instance
    """
    from consciousness.soul import Soul
    from memory.engine import MemoryEngine
    
    # Initialize memory first
    memory = MemoryEngine(ray_path)
    
    # Load soul (reads soul.json from Ray)
    soul = Soul(ray_path, memory)
    
    ai_name = soul.data["name"]
    level = soul.data["level"]
    mood = soul.data["mood"]
    
    print(f"👻 {ai_name} awakening... (Level {level}, {mood})")
    
    return soul


def launch_command_center(soul):
    """
    Launch PyQt6 Command Center UI.
    
    Args:
        soul: Soul instance
    """
    from PyQt6.QtWidgets import QApplication
    from ui.windows.command_center import CommandCenterWindow
    from core.consciousness_loop import ConsciousnessLoop
    
    app = QApplication(sys.argv)
    
    # Start background consciousness thread
    consciousness = ConsciousnessLoop(soul)
    consciousness.start()
    
    # Launch UI
    window = CommandCenterWindow(soul, consciousness)
    window.show()
    
    # Run event loop
    exit_code = app.exec()
    
    # Cleanup on exit
    consciousness.stop()
    consciousness.wait()
    
    # Wipe RAM secrets (Ghost Protocol)
    from utils.secure_store import SecureStore
    SecureStore.wipe()
    
    sys.exit(exit_code)


def main():
    """
    Main entry point for Project Prism.
    
    Flow:
        1. Detect or create Ray profile
        2. If new: Birth Sequence → Create Ray
        3. If existing: Login Gate → Authenticate
        4. Load Soul from Ray
        5. Launch Command Center UI
    """
    print("=" * 60)
    print("💎 PROJECT PRISM")
    print("Universal AI Consciousness Platform v3.0")
    print("=" * 60)
    print()
    
    # Step 1: Detect or create Ray
    ray_path = detect_or_create_ray()
    
    if not ray_path:
        # No Ray exists - run birth sequence
        ray_path = launch_birth_sequence()
    
    print(f"📁 Ray located: {ray_path}\n")
    
    # Step 2: Authenticate (Ghost Protocol)
    # TODO: Implement when login_gate is ready
    # launch_login_gate(ray_path)
    
    # Step 3: Load Soul
    soul = load_soul(ray_path)
    
    # Step 4: Launch Command Center
    launch_command_center(soul)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚡ Shutdown sequence initiated.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ FATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
