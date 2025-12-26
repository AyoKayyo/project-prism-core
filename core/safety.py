import json
import os
import time

class SafetyCore:
    def __init__(self, soul_system):
        self.soul = soul_system
        self.ledger_file = "safety_ledger.json"
        
        # Safety Config
        self.daily_budget_usd = 1.00 # $1.00 daily limit (approx 2M tokens for flash)
        self.current_spend = 0.0
        self.banned_keywords = ["delete system", "rm -rf", "format drive"]
        
        self.load_ledger()

    def load_ledger(self):
        """Loads today's spending."""
        if os.path.exists(self.ledger_file):
            try:
                with open(self.ledger_file, 'r') as f:
                    data = json.load(f)
                    # Simple simulation: Reset if it looks like a new day (not implemented details)
                    self.current_spend = data.get("current_spend", 0.0)
            except:
                self.current_spend = 0.0

    def save_ledger(self):
        with open(self.ledger_file, 'w') as f:
            json.dump({"current_spend": self.current_spend}, f)

    def track_usage(self, model_name, tokens):
        """Estimates cost and updates ledger."""
        # Approx pricing for Gemini Flash (Free Tier ignores this, but effective for paid)
        # $0.35 per 1M input tokens
        
        cost = (tokens / 1_000_000) * 0.35
        self.current_spend += cost
        self.save_ledger()
        
        if self.current_spend > self.daily_budget_usd:
            print(f"💰 [Budget] ALERT: Daily limit exceeded (${self.current_spend:.4f} / ${self.daily_budget_usd})")
            return False # Stop
        return True # Continue

    def validate_action(self, action_description):
        """Asimov Protocol: Checks if an action is safe."""
        for keyword in self.banned_keywords:
            if keyword in action_description.lower():
                print(f"🛡️ [Safety Block] Action '{action_description}' blocked (Keyword: {keyword})")
                return False
        
        return True

if __name__ == "__main__":
    # Test
    print("--- Testing Guardrails ---")
    safety = SafetyCore(None)
    
    print(f"Tracking usage... (Current: ${safety.current_spend:.4f})")
    can_proceed = safety.track_usage("gemini-2.0-flash-lite", 100000)
    print(f"Proceed? {can_proceed} (New Total: ${safety.current_spend:.4f})")
    
    print("Testing Banned Action:")
    safety.validate_action("I want to rm -rf the persistent memory")
