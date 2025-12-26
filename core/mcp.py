"""
Main Control Program (MCP) - The Safety Firewall

All AI actions pass through this gate for evaluation and enforcement.
"""

import json
from pathlib import Path
from enum import Enum
from typing import Dict, Optional, Callable
from dataclasses import dataclass


class SafetyTier(Enum):
    """Action safety classification."""
    GREEN = "green"   # Auto-execute (read-only, safe)
    YELLOW = "yellow" # Execute + notify
    RED = "red"       # Require approval


@dataclass
class ActionRequest:
    """Represents an action the AI wants to perform."""
    action_type: str
    parameters: Dict
    reason: str
    agent_name: str = "unknown"


class SafetyController:
    """
    Evaluates actions against safety tiers.
    
    Implements the Green/Yellow/Red classification system.
    """
    
    def __init__(self, config_path: Optional[Path] = None):
        """
        Initialize safety controller.
        
        Args:
            config_path: Path to safety_rules.json
        """
        if config_path is None:
            config_path = Path(__file__).parent.parent / "config" / "safety_rules.json"
        
        self.config_path = Path(config_path)
        self.rules = self._load_rules()
    
    def _load_rules(self) -> Dict:
        """Load safety rules from config."""
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️ [MCP] Failed to load safety rules: {e}")
            # Fallback to strict defaults
            return {
                "green_actions": ["chat", "read_file"],
                "yellow_actions": ["create_file", "modify_file"],
                "red_actions": ["delete_file", "system_command"]
            }
    
    def classify_action(self, action_type: str) -> SafetyTier:
        """
        Classify an action into a safety tier.
        
        Args:
            action_type: Type of action (e.g., "read_file")
            
        Returns:
            SafetyTier enum value
        """
        if action_type in self.rules.get("green_actions", []):
            return SafetyTier.GREEN
        elif action_type in self.rules.get("yellow_actions", []):
            return SafetyTier.YELLOW
        else:
            # Default to RED for unknown actions (safe by default)
            return SafetyTier.RED
    
    def is_blocked_keyword(self, command: str) -> bool:
        """
        Check if command contains blocked keywords.
        
        Args:
            command: Command string to check
            
        Returns:
            True if contains blocked keyword
        """
        blocked = self.rules.get("blocked_keywords", [])
        command_lower = command.lower()
        
        for keyword in blocked:
            if keyword.lower() in command_lower:
                print(f"🚫 [MCP] BLOCKED: Contains dangerous keyword '{keyword}'")
                return True
        
        return False


class SafetyMonitor:
    """
    Tracks API usage and enforces budget limits.
    """
    
    def __init__(self, ledger_path: Optional[Path] = None):
        """
        Initialize safety monitor.
        
        Args:
            ledger_path: Path to safety_ledger.json
        """
        if ledger_path is None:
            ledger_path = Path(__file__).parent.parent / "config" / "safety_ledger.json"
        
        self.ledger_path = Path(ledger_path)
        self.ledger = self._load_ledger()
        self.daily_budget = self.ledger.get("daily_budget_usd", 1.0)
        self.daily_spend = self.ledger.get("total_spent_today", 0.0)
    
    def _load_ledger(self) -> Dict:
        """Load safety ledger."""
        if self.ledger_path.exists():
            try:
                with open(self.ledger_path, 'r') as f:
                    return json.load(f)
            except Exception:
                pass
        
        # Create new ledger
        return {
            "ledger_version": "1.0",
            "date": self._get_today(),
            "daily_budget_usd": 1.0,
            "total_spent_today": 0.0,
            "transactions": []
        }
    
    def _save_ledger(self) -> None:
        """Save ledger to disk."""
        self.ledger_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.ledger_path, 'w') as f:
            json.dump(self.ledger, f, indent=2)
    
    def _get_today(self) -> str:
        """Get today's date."""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d")
    
    def _check_date_rollover(self) -> None:
        """Reset counters if new day."""
        today = self._get_today()
        if self.ledger.get("date") != today:
            print(f"📅 [MCP] New day detected. Resetting budget.")
            self.ledger["date"] = today
            self.ledger["total_spent_today"] = 0.0
            self.ledger["transactions"] = []
            self.daily_spend = 0.0
            self._save_ledger()
    
    def track_usage(self, model: str, input_tokens: int, output_tokens: int = 0) -> bool:
        """
        Track API usage and check against budget.
        
        Args:
            model: Model name (e.g., "gemini-2.0-flash")
            input_tokens: Input token count
            output_tokens: Output token count
            
        Returns:
            True if within budget, False if exceeded
        """
        self._check_date_rollover()
        
        # Calculate cost
        cost = self._calculate_cost(model, input_tokens, output_tokens)
        
        # Check budget
        if self.daily_spend + cost > self.daily_budget:
            remaining = self.daily_budget - self.daily_spend
            print(f"⚠️ [MCP] Budget exceeded! Spent: ${self.daily_spend:.4f}, "
                  f"Remaining: ${remaining:.4f}, Attempted: ${cost:.4f}")
            return False
        
        # Log transaction
        transaction = {
            "time": __import__("time").strftime("%H:%M:%S"),
            "model": model,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "cost_usd": cost
        }
        
        self.ledger["transactions"].append(transaction)
        self.ledger["total_spent_today"] += cost
        self.daily_spend += cost
        
        self._save_ledger()
        
        # Warn at 80% threshold
        if self.daily_spend >= self.daily_budget * 0.8:
            print(f"⚠️ [MCP] Warning: 80% of daily budget used (${self.daily_spend:.4f})")
        
        return True
    
    def _calculate_cost(self, model: str, input_tokens: int, output_tokens: int) -> float:
        """
        Calculate cost for API call.
        
        Args:
            model: Model name
            input_tokens: Input tokens
            output_tokens: Output tokens
            
        Returns:
            Cost in USD
        """
        # Load pricing from safety_rules.json
        config_path = Path(__file__).parent.parent / "config" / "safety_rules.json"
        try:
            with open(config_path, 'r') as f:
                rules = json.load(f)
                pricing = rules.get("budget", {}).get("models", {})
        except Exception:
            pricing = {}
        
        # Get model pricing (default to free for local models)
        model_pricing = pricing.get(model, {
            "input_per_1k_tokens": 0.0,
            "output_per_1k_tokens": 0.0
        })
        
        input_cost = (input_tokens / 1000) * model_pricing.get("input_per_1k_tokens", 0.0)
        output_cost = (output_tokens / 1000) * model_pricing.get("output_per_1k_tokens", 0.0)
        
        return input_cost + output_cost
    
    def get_budget_status(self) -> Dict:
        """
        Get current budget status.
        
        Returns:
            Dictionary with budget info
        """
        self._check_date_rollover()
        
        return {
            "daily_budget": self.daily_budget,
            "spent_today": self.daily_spend,
            "remaining": self.daily_budget - self.daily_spend,
            "percentage_used": (self.daily_spend / self.daily_budget) * 100 if self.daily_budget > 0 else 0,
            "transactions_today": len(self.ledger.get("transactions", []))
        }


class MCP:
    """
    Main Control Program - The central safety gate.
    
    All AI actions are routed through this controller.
    """
    
    def __init__(self):
        """Initialize MCP with safety controller and monitor."""
        self.controller = SafetyController()
        self.monitor = SafetyMonitor()
        self.pending_approvals = {}  # RED-tier actions awaiting approval
    
    def request_action(self, action: ActionRequest, 
                      approval_callback: Optional[Callable] = None) -> Optional[str]:
        """
        Request permission to perform an action.
        
        Args:
            action: ActionRequest object
            approval_callback: Function to call for RED-tier approval
            
        Returns:
            "approved", "executed", "blocked", or "pending"
        """
        # Classify action
        tier = self.controller.classify_action(action.action_type)
        
        print(f"🎯 [MCP] Action: {action.action_type} → Tier: {tier.value}")
        
        if tier == SafetyTier.GREEN:
            # Auto-approve
            return "approved"
        
        elif tier == SafetyTier.YELLOW:
            # Execute and notify
            print(f"🟡 [MCP] YELLOW: {action.action_type} - {action.reason}")
            return "approved"
        
        elif tier == SafetyTier.RED:
            # Require approval
            print(f"🔴 [MCP] RED: {action.action_type} - Requires approval")
            
            if approval_callback:
                approved = approval_callback(action)
                if approved:
                    print(f"✅ [MCP] User approved: {action.action_type}")
                    return "approved"
                else:
                    print(f"❌ [MCP] User denied: {action.action_type}")
                    return "blocked"
            else:
                # No callback - add to pending
                action_id = f"{action.action_type}_{len(self.pending_approvals)}"
                self.pending_approvals[action_id] = action
                return "pending"
        
        return "blocked"
    
    def check_budget(self, model: str, estimated_tokens: int) -> bool:
        """
        Check if action is within budget.
        
        Args:
            model: Model name
            estimated_tokens: Estimated token usage
            
        Returns:
            True if within budget
        """
        return self.monitor.track_usage(model, estimated_tokens)


if __name__ == "__main__":
    # Test
    print("--- Testing MCP ---\n")
    mcp = MCP()
    
    # Test GREEN action
    action1 = ActionRequest(
        action_type="read_file",
        parameters={"path": "test.txt"},
        reason="User requested file content"
    )
    print(f"Result: {mcp.request_action(action1)}\n")
    
    # Test YELLOW action
    action2 = ActionRequest(
        action_type="create_file",
        parameters={"path": "new.txt", "content": "Hello"},
        reason="Saving user content"
    )
    print(f"Result: {mcp.request_action(action2)}\n")
    
    # Test RED action
    action3 = ActionRequest(
        action_type="delete_file",
        parameters={"path": "important.txt"},
        reason="Cleanup requested"
    )
    print(f"Result: {mcp.request_action(action3)}\n")
    
    # Test budget
    print(f"Budget check (gemini-2.0-flash, 1000 tokens): "
          f"{mcp.check_budget('gemini-2.0-flash', 1000)}")
    
    print(f"\nBudget status: {mcp.monitor.get_budget_status()}")
