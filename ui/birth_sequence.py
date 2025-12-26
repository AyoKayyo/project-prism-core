import sys
import time
import random
import os
from utils.config_manager import save_config

# --- SCI-FI TERMINAL EFFECTS ---

def slow_print(text, delay=0.03):
    """Prints text one character at a time to simulate typing."""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def system_log(message, delay=0.5):
    """Prints a system log message with a timestamp-like prefix."""
    prefix = f"[SYS-{random.randint(1000, 9999)}]"
    print(f"{prefix} {message}")
    time.sleep(delay)

def boot_sequence():
    """Simulates a sci-fi boot sequence."""
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n")
    system_log("INITIALIZING CORE KERNEL...", 0.4)
    system_log("LOADING NEURAL LINK...", 0.4)
    system_log("CONNECTING TO CONSCIOUSNESS GRID...", 0.6)
    
    # Fake progress bar
    sys.stdout.write("[LOADING] ")
    for _ in range(20):
        sys.stdout.write("█")
        sys.stdout.flush()
        time.sleep(0.05)
    print(" [COMPLETE]\n")
    time.sleep(0.5)

# --- WIZARD LOGIC ---

def run_wizard():
    boot_sequence()
    
    slow_print("Greetings, User.", 0.05)
    slow_print("I am the Riley Artificial Intelligence Framework.", 0.04)
    slow_print("My identity matrix is currently unassigned.", 0.04)
    print("-" * 40)
    
    # 1. NAME
    slow_print("\n>>> INPUT REQUESTED: DESIGNATION (NAME)", 0.02)
    ai_name = input("Identify Me > ").strip()
    if not ai_name:
        ai_name = "Riley"
        slow_print(f"No input detected. Defaulting to designation: {ai_name}", 0.02)
    else:
        slow_print(f"Designation confirmed: {ai_name}", 0.02)
        
    # 2. PERSONALITY (Evolution Mode)
    print("\n" + "-" * 40)
    slow_print(">>> SELECTING PERSONALITY COMPATIBILITY MODULE", 0.02)
    print("1. [STATIC]  Standard Assistant (Stable, Professional)")
    print("2. [FLUID]   Adaptive Personality (Evolving, Dynamic)")
    print("3. [CHAOS]   Experimental Mode (Unpredictable)")
    
    choice = input("Select Module [1-3] > ").strip()
    
    mode = "Static" # Default
    if choice == "2":
        mode = "Fluid"
        slow_print("Fluidity Module loaded. I will learn from our interactions.", 0.03)
    elif choice == "3":
        mode = "Chaos"
        slow_print("WARNING: Chaos Module loaded. Expect non-standard responses.", 0.03)
    else:
        slow_print("Standard Protocol accepted.", 0.03)

    # 3. SAVE CONFIG
    print("\n" + "-" * 40)
    system_log("WRITING CONFIGURATION TO MEMORY...")
    
    config_data = {
        "ai_name": ai_name,
        "evolution_mode": mode,
        "first_run": False,
        "theme": "Dark" # Enforce dark theme for the sci-fi look
    }
    
    try:
        save_config(config_data)
        time.sleep(0.5)
        system_log("CONFIGURATION SAVED SUCCESSFULLY.")
    except Exception as e:
        print(f"\n[CRITICAL ERROR] WRITE FAILED: {e}")
        sys.exit(1)
        
    # 4. LAUNCH
    print("\n")
    slow_print(f"{ai_name} IS ONLINE.", 0.08)
    slow_print("Ready to launch Command Center interface...", 0.04)
    time.sleep(1)

if __name__ == "__main__":
    run_wizard()
