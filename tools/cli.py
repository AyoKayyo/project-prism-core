#!/usr/bin/env python3
"""
Riley CLI - Command-line interface for Riley Consciousness Lab
"""
import argparse
import json
import sys
import os

def load_soul():
    """Load Riley's soul data"""
    if os.path.exists("soul.json"):
        with open("soul.json", 'r') as f:
            return json.load(f)
    return None

def display_status():
    """Display Riley's current status"""
    soul = load_soul()
    if not soul:
        print("❌ Riley hasn't been initialized yet. Run: python consciousness.py")
        return
    
    print("\n👻 Riley Consciousness Status\n" + "="*50)
    print(f"Name: {soul.get('name', 'Unknown')}")
    print(f"Level: {soul.get('level', 0)}")
    print(f"XP: {soul.get('xp', 0)} / {soul.get('xp_to_next_level', 100)}")
    print(f"Mood: {soul.get('mood', 'Unknown')}")
    print(f"Traits: {', '.join(soul.get('traits', []))}")
    print(f"Version: {soul.get('version', 'Unknown')}")
    print("="*50 + "\n")

def check_budget():
    """Check current API budget usage"""
    if os.path.exists("safety_ledger.json"):
        with open("safety_ledger.json", 'r') as f:
            ledger = json.load(f)
        current = ledger.get("current_spend", 0)
        print(f"\n💰 Budget Status\n" + "="*50)
        print(f"Current Spend: ${current:.6f}")
        print(f"Daily Limit: $1.00")
        print(f"Remaining: ${max(0, 1.0 - current):.6f}")
        print("="*50 + "\n")
    else:
        print("No budget data found.")

def view_memories(limit=10):
    """View recent episodic memories"""
    print(f"\n📓 Recent Memories (last {limit})\n" + "="*50)
    # This would require querying ChromaDB - simplified for now
    print("Memory viewing requires database integration.")
    print("Check db/ folder for ChromaDB persistence.")
    print("="*50 + "\n")

def reset_soul():
    """Reset Riley's soul to Level 1"""
    confirm = input("⚠️  This will reset Riley to Level 1. Continue? (yes/no): ")
    if confirm.lower() == 'yes':
        if os.path.exists("soul.json"):
            os.remove("soul.json")
        if os.path.exists("safety_ledger.json"):
            os.remove("safety_ledger.json")
        print("✅ Riley has been reset. Run consciousness.py to reinitialize.")
    else:
        print("❌ Reset cancelled.")

def main():
    parser = argparse.ArgumentParser(
        description="Riley Consciousness Lab CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  riley_cli.py status        # Show Riley's current state
  riley_cli.py budget        # Check API budget usage
  riley_cli.py memories      # View recent memories
  riley_cli.py reset         # Reset Riley to Level 1
        """
    )
    
    parser.add_argument(
        'command',
        choices=['status', 'budget', 'memories', 'reset'],
        help='Command to execute'
    )
    
    parser.add_argument(
        '--limit',
        type=int,
        default=10,
        help='Limit for memories command (default: 10)'
    )
    
    args = parser.parse_args()
    
    if args.command == 'status':
        display_status()
    elif args.command == 'budget':
        check_budget()
    elif args.command == 'memories':
        view_memories(args.limit)
    elif args.command == 'reset':
        reset_soul()

if __name__ == "__main__":
    main()
