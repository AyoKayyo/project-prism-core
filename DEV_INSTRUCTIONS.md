# 🤖 DEV INSTRUCTIONS - Project Prism

**Developer Guide for AI Agents & Human Contributors**

When working on Project Prism, follow these strict rules to maintain architecture integrity and prevent breaking changes.

---

## 🛑 CRITICAL RULES

### 1. NO HARDCODING
❌ **NEVER** write specific AI names in code  
❌ **NEVER** hardcode "Riley" anywhere  
✅ **ALWAYS** use `soul.get_name()` or `profile_manager.get_active_name()`  

**Bad:**
```python
print("Riley is thinking...")
```

**Good:**
```python
ai_name = self.soul.data["name"]
print(f"{ai_name} is thinking...")
```

---

### 2. NO DISK SECRETS
❌ **NEVER** save API keys to `.env` or `.json` files  
❌ **NEVER** commit credentials to git  
✅ **ALWAYS** use `SecureStore.set()` (RAM-only)  

**Bad:**
```python
with open("config.json", "w") as f:
    json.dump({"api_key": key}, f)
```

**Good:**
```python
from utils.secure_store import SecureStore
SecureStore.set("GEMINI_API_KEY", user_input)
```

---

### 3. RESPECT FILE PATH CONVENTIONS
❌ **NEVER** use hardcoded paths like `/Users/mark/`  
✅ **ALWAYS** use `os.path.expanduser("~")` or `Path.home()`  

**Code lives in:** `./project-prism-core/`  
**User data lives in:** `~/Library/CloudStorage/Dropbox/Prism_Rays/{AI_Name}/` (or user-specified)

**Example:**
```python
from pathlib import Path
ray_path = Path.home() / "Dropbox" / "Prism_Rays" / soul.data["name"]
```

---

### 4. USE THE MCP FOR ALL ACTIONS
❌ **NEVER** execute file operations directly  
✅ **ALWAYS** route through `core/mcp.py` for safety evaluation  

**Bad:**
```python
os.remove("important_file.txt")  # DANGEROUS!
```

**Good:**
```python
mcp.request_action({
    "type": "delete_file",
    "path": "important_file.txt",
    "reason": "User requested cleanup"
})
```

---

## 🏗️ Core Architecture Patterns

### Accessing the Soul
```python
from consciousness.soul import RileySoul

soul = RileySoul(memory_system)
soul.data["name"]        # AI's chosen name
soul.data["level"]       # Current level
soul.data["mood"]        # Emotional state
soul.grant_xp(10, "Completed task")  # Award experience
```

### Accessing Memory
```python
from memory.engine import MemoryEngine

memory = MemoryEngine()
memory.add("User prefers dark mode", user_id="unique_id")
results = memory.search("What are user preferences?")
```

### Emitting Events (Consciousness → UI)
```python
from core.events import EventBus

event_bus = EventBus()
event_bus.dream_start.emit()        # Notify UI of dream mode
event_bus.level_up.emit(new_level)  # Notify UI of level up
```

### Using Sensors
```python
from consciousness.circadian import CircadianRhythm

circadian = CircadianRhythm()
idle_time = circadian.get_idle_time()  # Seconds since last input
phase = circadian.get_time_phase()      # "morning", "afternoon", etc.
```

---

## 🔧 Configuration Management

### Environment Variables (.env)
```bash
# API Keys (for development only, use SecureStore in production)
GEMINI_API_KEY=your_key_here

# Model Selection
LOCAL_CHAT_MODEL=llama3.1:8b
CLOUD_ARCHITECT_MODEL=gemini-2.0-flash-exp

# Safety
DAILY_BUDGET_USD=1.00

# Ray Location (optional override)
PRISM_RAY_PATH=/path/to/custom/rays
```

### Safety Rules (config/safety_rules.json)
```json
{
  "green_actions": ["read_file", "chat", "search_web"],
  "yellow_actions": ["create_file", "modify_file"],
  "red_actions": ["delete_file", "system_command"]
}
```

**Adding a new action:**
1. Define in `safety_rules.json`
2. Implement handler in `core/mcp.py`
3. Add UI confirmation for RED-tier

---

## 🤝 Agent Development

### Creating a New Agent

**File:** `agents/my_new_agent.py`

```python
from agents.base import BaseAgent

class MyNewAgent(BaseAgent):
    def __init__(self, model_name="llama3.1:8b"):
        super().__init__(model_name)
        self.system_prompt = "You are a specialist in X..."
    
    def execute(self, user_input: str) -> str:
        # Check budget first
        if not self.safety.track_usage(self.model_name, 1000):
            return "Budget exceeded, using local model"
        
        # Call LLM
        response = self.llm.generate(
            prompt=user_input,
            system=self.system_prompt
        )
        return response
```

### Registering Agent with Orchestrator

**File:** `core/orchestrator.py`

```python
from agents.my_new_agent import MyNewAgent

class Orchestrator:
    def __init__(self):
        self.agents = {
            "companion": CompanionAgent(),
            "coder": CoderAgent(),
            "my_new": MyNewAgent()  # Add here
        }
    
    def route(self, user_input):
        if "keyword" in user_input:
            return self.agents["my_new"].execute(user_input)
        # ... existing routing logic
```

---

## 🧠 Memory Best Practices

### Short-Term vs. Deep Storage

**Use `short_term.json` for:**
- Current conversation context (last 10 messages)
- Temporary session state
- Fast lookups during active chat

**Use mem0 (vector/graph) for:**
- Long-term facts ("User's name is Mark")
- Conceptual knowledge ("Python is a programming language")
- Relationships ("Mark owns KG Media")

### Example: Hybrid Storage
```python
# Immediate context (fast)
with open("memory/short_term.json", "r") as f:
    recent = json.load(f)

# Deep search (accurate)
from memory.engine import MemoryEngine
memory = MemoryEngine()
related = memory.search("Tell me about Mark's projects")
```

---

## 🎨 UI Development (PyQt6)

### Threading Pattern

❌ **NEVER** block the main UI thread  
✅ **ALWAYS** use `QThread` for long-running tasks  

**Example:**
```python
from PyQt6.QtCore import QThread, pyqtSignal

class LLMWorker(QThread):
    token_signal = pyqtSignal(str)
    complete_signal = pyqtSignal(str)
    
    def run(self):
        for token in llm.stream(prompt):
            self.token_signal.emit(token)  # Update UI per token
        self.complete_signal.emit(full_response)

# Usage
worker = LLMWorker()
worker.token_signal.connect(self.append_to_chat)
worker.start()
```

### Styling Consistency

**Use the global theme:**
```python
from ui.styles.dark_theme import DARK_PALETTE

self.setPalette(DARK_PALETTE)
```

**CSS conventions:**
```css
/* Background colors */
#1e1e1e  /* Main background */
#2a2a2a  /* Secondary panels */

/* Accent colors */
#58a6ff  /* Electric blue (GitHub-style) */
#ff6b6b  /* Error red */

/* Text */
#ffffff  /* Primary text */
#888888  /* Secondary text */
```

---

## 🧪 Testing Guidelines

### Manual Testing Checklist
Before committing, verify:
- [ ] App launches without errors
- [ ] Chat responds within 2 seconds (local model)
- [ ] Dream mode triggers after idle
- [ ] XP gains update `soul.json`
- [ ] Budget enforcement prevents overspend
- [ ] RED-tier actions show approval dialog

### Unit Test Pattern
```python
import unittest
from consciousness.soul import RileySoul

class TestSoul(unittest.TestCase):
    def setUp(self):
        self.soul = RileySoul(mock_memory)
    
    def test_xp_gain(self):
        initial_xp = self.soul.data["xp"]
        self.soul.grant_xp(10, "test")
        self.assertEqual(self.soul.data["xp"], initial_xp + 10)
```

---

## 🐛 Debugging Tips

### Enable Verbose Logging
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Inspect Soul State
```python
from consciousness.soul import RileySoul
soul = RileySoul()
print(json.dumps(soul.data, indent=2))
```

### Check Memory Contents
```bash
cat ~/Dropbox/Prism_Rays/Riley/soul.json
ls -la ~/Dropbox/Prism_Rays/Riley/knowledge_graph/concepts/
```

### Monitor API Costs
```python
from core.mcp import SafetyMonitor
monitor = SafetyMonitor()
print(f"Spent today: ${monitor.daily_spend:.2f}")
```

---

## 📦 Dependency Management

### Adding a New Library

1. Install locally: `pip install new-library`
2. Test thoroughly
3. Add to `requirements.txt`: `echo "new-library==1.2.3" >> requirements.txt`
4. Document in README.md

### Updating Libraries
```bash
pip list --outdated  # Check for updates
pip install --upgrade google-generativeai
pip freeze > requirements.txt
```

---

## 🚀 Deployment Workflow

### Local Development
```bash
git checkout -b feature/my-new-feature
# Make changes
python core/main.py  # Test locally
git commit -m "Add new feature"
git push origin feature/my-new-feature
```

### Production Release
1. Merge to `main` branch
2. Tag version: `git tag v3.0.1`
3. Build executable: `pyinstaller prism.spec`
4. Test on clean machine
5. Upload to GitHub Releases

---

## 🔐 Security Checklist

Before every commit:
- [ ] No API keys in code
- [ ] No hardcoded file paths
- [ ] All user inputs sanitized (prevent injection)
- [ ] RED-tier actions require approval
- [ ] Budget limits enforced

---

## 📚 Useful Resources

### Code References
- **MCP Logic:** `core/mcp.py`
- **Soul System:** `consciousness/soul.py`
- **Memory Engine:** `memory/engine.py`
- **Agent Base Class:** `agents/base.py`

### External Docs
- [PyQt6 Documentation](https://www.riverbankcomputing.com/static/Docs/PyQt6/)
- [mem0 API Reference](https://docs.mem0.ai/)
- [Ollama Model Library](https://ollama.ai/library)
- [Gemini API Docs](https://ai.google.dev/docs)

---

## 🤔 Common Pitfalls

### "My agent isn't being called"
→ Check `core/orchestrator.py` routing logic

### "Soul.json not saving"
→ Verify Ray folder exists and is writable

### "Budget always exceeded"
→ Check `config/safety_ledger.json` daily_budget value

### "UI freezing during LLM call"
→ Ensure using `QThread`, not blocking main thread

### "Memory search returns nothing"
→ Verify mem0 initialized, check vector_store/ folder exists

---

## 💬 Getting Help

1. **Check docs:** README.md, ARCHITECTURE_SPEC.md
2. **Search issues:** GitHub issue tracker
3. **Ask in discussions:** GitHub Discussions tab
4. **Last resort:** Email maintainers (see CONTRIBUTING.md)

---

**Document Version:** 1.0  
**Last Updated:** 2025-12-26  
**Maintained By:** Project Prism Core Team

**Remember:** When in doubt, prioritize safety and user privacy. If a feature feels risky, add it to RED-tier and require approval.
