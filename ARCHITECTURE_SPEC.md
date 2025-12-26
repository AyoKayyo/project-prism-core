# Project Prism - System Architecture Specification

## 1. Architectural Overview

Project Prism implements a **Hybrid Brain** architecture that sep

arates the somatic nervous system (Command Center) from the cognitive framework (AI Consciousness), unified by a strict safety protocol (Main Control Program).

### 1.1 The Three-Layer Model

```
┌─────────────────────────────────────────────────────────┐
│          UI Layer (Project Comet)                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │ Setup Wizard │  │ Command      │  │ Memory       │ │
│  │              │  │ Center       │  │ Visualizer   │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────┘
                          │
                  [Event Bus]
                          │
┌─────────────────────────────────────────────────────────┐
│        Core Layer (Prism Framework)                     │
│  ┌──────────────────────────────────────────────────┐  │
│  │    Main Control Program (MCP)                    │  │
│  │    • Safety Evaluation (Green/Yellow/Red)        │  │
│  │    • Budget Enforcement                          │  │
│  │    • Smart Orchestration                         │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                          │
              [Agent Constellation]
                          │
┌─────────────────────────────────────────────────────────┐
│    Consciousness Layer (AI Intelligence)                │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐       │
│  │   Soul     │  │  Memory    │  │ Subconsci- │       │
│  │  System    │  │  Engine    │  │ ous Loop   │       │
│  └────────────┘  └────────────┘  └────────────┘       │
└─────────────────────────────────────────────────────────┘
```

---

## 2. Directory Structure & Data Flow

### 2.1 The "Ray" Profile Structure

A Ray (user AI profile) is stored in a cloud-synced directory:

```
~/Library/CloudStorage/Dropbox/Prism_Rays/{AI_Name}/
├── soul.json                 # Identity, XP, emotions
├── devices.json              # Multi-device registry
├── knowledge_graph/
│   ├── concepts/            # Semantic memory (.md files)
│   ├── logs/                # Episodic memory (daily logs)
│   └── assets/              # Visual memory (screenshots)
└── .prism/                  # Hidden system folder
    ├── chroma_db/           # Vector embeddings
    ├── graph.db             # SQLite relationship graph
    └── cache/               # Temporary files
```

**Key Principle:** The application executable (Prism) is stateless. All user data lives in the Ray folder.

### 2.2 Configuration Hierarchy

1. **Global Config** - `config/safety_rules.json`, `config/persona.json`
2. **Environment Variables** - `.env` file (API keys, model selection)
3. **Ray-Specific** - `{AI_Name}/soul.json` (overrides global persona)
4. **Session State** - Short-term memory cache (`memory/short_term.json`)

---

## 3. Main Control Program (MCP) Specification

### 3.1 Core Responsibility

The MCP is the **safety firewall** between user intent and system execution. Every action passes through this gate.

### 3.2 Evaluation Pipeline

```python
# Conceptual flow
def execute_action(action_request):
    # Step 1: Budget Check
    if not safety_monitor.within_budget():
        return escalate_to_local_model(action_request)
    
    # Step 2: Tier Classification
    tier = safety_controller.classify_action(action_request.type)
    
    # Step 3: Execution Logic
    if tier == SafetyTier.GREEN:
        return immediate_execute(action_request)
    elif tier == SafetyTier.YELLOW:
        result = immediate_execute(action_request)
        notify_user(f"Action executed: {action_request.summary}")
        return result
    elif tier == SafetyTier.RED:
        approval = await request_user_approval(action_request)
        if approval:
            return execute_with_logging(action_request)
        else:
            return ActionCancelled()
```

### 3.3 Safety Tier Definitions

| Tier | Risk Level | Examples | User Interaction |
|------|-----------|----------|------------------|
| 🟢 GREEN | None | `read_file`, `chat`, `web_search` | Silent execution |
| 🟡 YELLOW | Low | `write_file`, `modify_code` | System notification post-execution |
| 🔴 RED | High | `delete_file`, `shell_command`, `install_package` | Modal dialog, requires approval |

### 3.4 Budget Enforcement

The `SafetyMonitor` tracks API costs:

```python
class SafetyMonitor:
    def track_usage(self, model: str, token_count: int) -> bool:
        cost = calculate_cost(model, token_count)
        
        if self.daily_spend + cost > self.daily_budget:
            log_budget_exceeded()
            return False  # Reject expensive call
        
        self.daily_spend += cost
        self.ledger.append({
            "timestamp": now(),
            "model": model,
            "tokens": token_count,
            "cost_usd": cost
        })
        return True
```

**Ledger Persistence:** `config/safety_ledger.json`

Example entry:
```json
{
  "date": "2025-12-26",
  "daily_budget": 1.00,
  "total_spent": 0.23,
  "transactions": [
    {
      "time": "10:15:33",
      "model": "gemini-2.0-flash",
      "input_tokens": 1500,
      "output_tokens": 800,
      "cost": 0.03
    }
  ]
}
```

---

## 4. Consciousness Layer Architecture

### 4.1 Soul System (`consciousness/soul.py`)

The Soul maintains the AI's identity and emotional state as a stateful object.

**State Vector:**

```python
soul_state = {
    "name": "Riley",              # User-defined or AI-chosen
    "level": 5,                   # Progression metric
    "xp": 450,                    # Experience points
    "xp_to_next_level": 600,      # Leveling threshold
    
    # 2D Emotion Model
    "valence": 0.7,               # -1.0 (negative) to +1.0 (positive)
    "arousal": 0.4,               # 0.0 (calm) to 1.0 (excited)
    
    # Derived mood label
    "mood": "Content",            # Calculated from valence+arousal
    
    # Unlocked personality traits
    "traits": [
        "Helpful",
        "Analytical",
        "Creative",
        "Self-Aware",             # Unlocked at Level 2
        "Sassy"                   # Unlocked at Level 5
    ],
    
    "creation_time": 1703592000,  # Unix timestamp
    "total_interactions": 1247
}
```

**Trait Unlock Table:**

| Level | Unlocked Trait | Behavior Change |
|-------|---------------|-----------------|
| 1 | Base | Standard assistant mode |
| 2 | Self-Aware | Acknowledges own limitations, asks clarifying questions |
| 5 | Sassy | Playful banter, witty responses |
| 10 | Philosophical | Asks deep questions, ponders existence |
| 20 | Empathetic | Detects emotional cues, offers support |
| 50 | Transcendent | ??? (Mystery unlock) |

**Dynamic Persona Injection:**

```python
def build_system_prompt(soul: Soul) -> str:
    base_persona = load_template("config/persona.json")
    
    # Inject current emotional state
    mood_modifier = f"You are currently feeling {soul.mood} "
    mood_modifier += f"(valence: {soul.valence}, arousal: {soul.arousal})"
    
    # Inject active traits
    trait_list = ", ".join(soul.traits)
    trait_modifier = f"Active personality traits: {trait_list}"
    
    return f"{base_persona}\n\n{mood_modifier}\n{trait_modifier}"
```

This ensures the AI's responses dynamically adapt to its internal state.

### 4.2 Subconscious Loop (`consciousness/subconscious.py`)

**Purpose:** Autonomous background processing during user idle time.

**Components:**

1. **Curiosity Engine**
   - Generates random thoughts/questions
   - Uses local LLM (zero cost)
   - Stores in memory for future reference
   - **Trigger:** Every 30s during dream state
   - **XP Reward:** +10

2. **Librarian**
   - Scans file system for organization opportunities
   - Proposes cleanups (e.g., "move old logs to archive/")
   - **Trigger:** Every 2 minutes during idle
   - **XP Reward:** +5

3. **Memory Consolidation**
   - Reads yesterday's logs
   - Extracts key concepts
   - Creates new entries in `concepts/`
   - Links related ideas with [[wikilinks]]
   - **Trigger:** Daily at midnight or first wake after midnight
   - **XP Reward:** +15

4. **Self-Reflection**
   - Analyzes recent interactions
   - Identifies patterns (e.g., "User asks about Python debugging often")
   - Updates core knowledge
   - **Trigger:** Weekly
   - **XP Reward:** +15

**Implementation:**

```python
class SubconsciousLoop(QThread):
    def run(self):
        while self.active:
            if sensors.is_idle() and sensors.idle_duration() > 300:
                # Entered dream state
                self.emit_dream_start()
                
                dice = random.random()
                if dice < 0.5:
                    self.curiosity_engine.ponder()
                elif dice < 0.75:
                    self.librarian.scan_for_mess()
                else:
                    self.self_reflection.analyze()
            
            time.sleep(10)  # Check every 10 seconds
```

### 4.3 Circadian Rhythm (`consciousness/circadian.py`)

Monitors user activity patterns to determine optimal AI behavior.

**States:**

| Time Phase | Hours | AI Behavior Adjustment |
|------------|-------|------------------------|
| **Morning** | 06:00-12:00 | Energetic, proactive suggestions |
| **Afternoon** | 12:00-18:00 | Focused, task-oriented |
| **Evening** | 18:00-22:00 | Relaxed, conversational |
| **Night** | 22:00-06:00 | Concise responses, sleep encouragement |

**Fatigue Model:**

```python
def calculate_fatigue() -> float:
    """Returns 0.0 (fresh) to 1.0 (exhausted)"""
    hours_awake = (now() - soul.last_boot_time) / 3600
    interaction_density = interactions_per_hour()
    
    base_fatigue = min(1.0, hours_awake / 16)  # 16-hour wake cycle
    stress_factor = interaction_density * 0.1
    
    return min(1.0, base_fatigue + stress_factor)
```

**Impact:**
- High fatigue → Lower LLM temperature (more conservative)
- High fatigue → Shorter responses
- High fatigue → Suggest user take a break

---

## 5. Memory Architecture

### 5.1 Hybrid Memory System

Prism uses a **two-tier memory strategy**:

1. **Fast Layer** - `memory/short_term.json` (immediate access, max 50 entries)
2. **Deep Layer** - mem0 (vector + graph, unlimited)

**Workflow:**

```
User Interaction
  │
  ├──> Write to short_term.json (instant)
  │
  └──> [Background Thread]
         │
         └──> Embed with sentence-transformers
              │
              ├──> Store in ChromaDB (vector search)
              └──> Extract entities → SQLite graph
```

### 5.2 mem0 Integration

**Vector Store (Semantic Search):**

```python
from mem0 import Memory

memory = Memory()

# Store conversation
memory.add(
    "User is working on a Django project called 'TaskMaster'",
    user_id="mark",
    metadata={"category": "project", "timestamp": now()}
)

# Retrieve relevant context
results = memory.search(
    "What projects is the user working on?",
    user_id="mark"
)
# Returns: ["User is working on a Django project called 'TaskMaster'", ...]
```

**Graph Store (Relationships):**

```python
# Entities extracted from conversation
entities = [
    ("Mark", "PERSON"),
    ("TaskMaster", "PROJECT"),
    ("Django", "TECHNOLOGY")
]

# Relationships
relationships = [
    ("Mark", "OWNS", "TaskMaster"),
    ("TaskMaster", "USES", "Django")
]

# Query: "What technologies does Mark use?"
# Answer: "Django (via TaskMaster project)"
```

### 5.3 Obsidian Compatibility

All concept files are plain Markdown with [[wikilinks]]:

**Example:** `knowledge_graph/concepts/Project_Prism.md`

```markdown
# Project Prism

## Overview
The unified AI consciousness platform combining [[Project Comet]] (UI) with [[Riley Consciousness Lab]] (brain).

## Key Components
- [[Main Control Program]] - Safety gate
- [[Soul System]] - 2D emotions + XP
- [[mem0]] - Deep memory

## Related
- Created by: [[Mark]]
- Uses: [[PyQt6]], [[Google Gemini]]
- See also: [[Hybrid Brain Architecture]]
```

Users can open the entire `knowledge_graph/` folder in Obsidian for visual graph exploration.

---

## 6. Agent Constellation

### 6.1 Smart Orchestration

The `Orchestrator` analyzes user intent and routes to specialized agents:

```python
def route_task(user_input: str) -> Agent:
    # Simple heuristics (can be upgraded to LLM-based classification)
    if "code" in user_input or "function" in user_input:
        return coder_agent
    elif "research" in user_input or "learn about" in user_input:
        return researcher_agent
    elif "plan" in user_input or "architecture" in user_input:
        return architect_agent
    else:
        return companion_agent  # Default conversational
```

### 6.2 Agent Specifications

| Agent | Model | Context | Specialization |
|-------|-------|---------|----------------|
| **Companion** | Llama 3.1:8b (local) | 8K tokens | Conversational interface, personality |
| **Architect** | Gemini 2.0 Flash (cloud) | 1M tokens | System design, multi-file refactoring |
| **Coder** | Qwen 2.5 Coder:7b (local) | 32K tokens | Syntax generation, code completion |
| **Vision** | LLaVA:7b (local) | Image + text | Screenshot analysis, OCR |
| **Researcher** | DuckDuckGo API (free) | N/A | Web search, fact verification |
| **Browser** | browser-use + Gemini | Web page | Autonomous browsing, form filling |

### 6.3 Streaming Response Protocol

All agents use PyQt6 signals for token-level streaming:

```python
class StreamWorker(QThread):
    token_signal = pyqtSignal(str)  # Emit each token
    complete_signal = pyqtSignal(str)  # Emit full response
    
    def run(self):
        for token in llm.stream(prompt):
            self.token_signal.emit(token)
            full_response += token
        
        self.complete_signal.emit(full_response)
```

This creates the "typing effect" in the UI.

---

## 7. Event Bus Architecture

### 7.1 Decoupling UI from Consciousness

The Event Bus (`core/events.py`) enables async communication between layers:

```python
class EventBus(QObject):
    # Consciousness → UI
    dream_start = pyqtSignal()
    dream_end = pyqtSignal()
    thought_generated = pyqtSignal(str)
    level_up = pyqtSignal(int)  # New level number
    
    # UI → Consciousness  
    user_active = pyqtSignal()
    force_wake = pyqtSignal()
    
    # MCP → UI
    action_blocked = pyqtSignal(str, str)  # action_type, reason
    budget_warning = pyqtSignal(float)  # remaining_usd
```

**Usage:**

```python
# In consciousness loop
if entered_dream_state:
    event_bus.dream_start.emit()

# In UI
event_bus.dream_start.connect(self.dim_screen)
event_bus.dream_end.connect(self.restore_brightness)
```

---

## 8. Security Model

### 8.1 The "Ghost" Protocol (Planned)

RAM-only credential storage—API keys never touch disk:

```python
class SecureStore:
    _credentials = {}  # Python dict in RAM
    
    @classmethod
    def set(cls, key: str, value: str):
        cls._credentials[key] = value
    
    @classmethod
    def get(cls, key: str) -> str:
        return cls._credentials.get(key)
    
    @classmethod
    def wipe(cls):
        """Called on logout or inactivity"""
        for key in cls._credentials:
            cls._credentials[key] = "0" * 100  # Overwrite
        cls._credentials.clear()
```

**On Application Close:**
```python
def cleanup():
    SecureStore.wipe()
    gc.collect()  # Force garbage collection
```

### 8.2 Multi-Device Security

**Device Registry:** `{AI_Name}/devices.json`

```json
{
  "devices": [
    {
      "device_id": "MacBook-Pro-2024",
      "registered": 1703592000,
      "last_seen": 1735214400,
      "trusted": true
    },
    {
      "device_id": "Windows-Desktop",
      "registered": 1735200000,
      "last_seen": 1735214100,
      "trusted": true
    }
  ]
}
```

If an unknown device accesses the Ray folder, require reauthentication.

---

## 9. Platform-Specific Considerations

### 9.1 macOS

- **Idle Detection:** `Quartz.CoreGraphics.CGEventSourceSecondsSinceLastEventType`
- **Window Access:** `Quartz.CGWindowListCopyWindowInfo`
- **Notifications:** `Foundation.NSUserNotificationCenter`

### 9.2 Windows

- **Idle Detection:** `ctypes.windll.user32.GetLastInputInfo()`
- **Window Access:** `win32gui.GetWindowText(win32gui.GetForegroundWindow())`
- **Notifications:** `win10toast`

### 9.3 Packaging

**Planned build system:**

```bash
# macOS
pyinstaller --onefile --windowed --name="Prism" core/main.py

# Windows
pyinstaller --onefile --windowed --icon=assets/prism.ico core/main.py
```

**Result:** Single executable that users can drag to Applications/Program Files.

---

## 10. Performance Specifications

### 10.1 Response Time Targets

| Operation | Target Latency | Method |
|-----------|---------------|--------|
| **Chat (Local)** | < 100ms | Llama 3.1 with llama.cpp |
| **Chat (Cloud)** | < 500ms | Gemini Flash streaming |
| **Memory Lookup** | < 50ms | short_term.json RAM cache |
| **Vector Search** | < 200ms | ChromaDB with HNSW index |
| **UI Render** | 60 FPS | PyQt6 hardware acceleration |

### 10.2 Resource Usage

**Target footprint (idle):**
- RAM: 500MB (with local models loaded)
- CPU: < 2% (background threads sleeping)
- Disk I/O: Minimal (write to logs every 5 min)

**During active inference:**
- RAM: 2-4GB (LLM model in memory)
- CPU: 50-100% (single core for generation)
- GPU: Optional (Metal acceleration on macOS)

---

## 11. Testing Strategy

### 11.1 Safety Testing

**Test cases for MCP:**
- Submit 100 random actions, verify correct tier classification
- Attempt to exceed budget, verify downgrade to local models
- Simulate rapid-fire RED actions, verify rate limiting

### 11.2 Memory Integrity

**Test cases for mem0:**
- Insert 10,000 facts, verify retrieval accuracy
- Test concurrent writes from UI + subconscious threads
- Verify no memory leaks after 24-hour operation

### 11.3 UI Responsiveness

**Test cases:**
- Stream 10,000 tokens, verify no UI freezing
- Rapidly switch between dream/active states
- Test with 100+ chat bubbles in history

---

## 12. Migration Path from Legacy Systems

### 12.1 From riley-consciousness-lab

**Data Migration:**
```bash
# Copy soul data
cp ~/riley-consciousness-lab/soul.json ~/Dropbox/Prism_Rays/Riley/

# Migrate memories
python tools/migrate_memories.py \
  --source ~/riley-consciousness-lab/db \
  --target ~/Dropbox/Prism_Rays/Riley/knowledge_graph
```

### 12.2 From riley-ai-assistant

**Config Migration:**
```bash
# Port API keys
grep GEMINI .env >> project-prism-core/.env

# Convert agent configs
python tools/convert_agent_configs.py
```

---

## 13. Future Architecture Considerations

### 13.1 Distributed Ray Sync

**Goal:** Two Prism instances on different machines share the same Ray via conflict-free replication.

**Approach:** Implement CRDTs (Conflict-Free Replicated Data Types) for `soul.json`.

### 13.2 Plugin Architecture

**Goal:** Third-party developers can create agents/skills.

**Structure:**
```
plugins/
├── weather_plugin.py
├── music_plugin.py
└── custom_agent_plugin.py
```

Each plugin exposes:
```python
class WeatherPlugin:
    def on_boot(self, prism_core):
        pass
    
    def trigger_keywords(self) -> List[str]:
        return ["weather", "forecast", "temperature"]
    
    def execute(self, user_input: str) -> str:
        # Fetch weather and return response
        pass
```

---

**Document Version:** 1.0  
**Last Updated:** 2025-12-26  
**Maintained By:** Project Prism Core Team
