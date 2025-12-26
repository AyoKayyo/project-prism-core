#!/usr/bin/env python3
"""
Quick Start Launcher for Project Prism

Usage: python launch_prism.py
"""

import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

def check_dependencies():
    """Check if critical dependencies are installed."""
    missing = []
    
    try:
        import psutil
    except ImportError:
        missing.append("psutil")
    
    try:
        import dotenv
    except ImportError:
        missing.append("python-dotenv")
    
    if missing:
        print("❌ Missing dependencies:")
        for dep in missing:
            print(f"   - {dep}")
        print("\n📦 Install with: pip install " + " ".join(missing))
        return False
    
    return True


def main():
    """Launch Project Prism."""
    print("💎 Launching Project Prism...\n")
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Import and run main
    try:
        from core.main import main as prism_main
        prism_main()
    except Exception as e:
        print(f"\n❌ Launch failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
