# 💡 IDEAS BACKLOG - Project Prism

**Future Vision & Unimplemented Features**

This document tracks features that have been conceptualized but **not yet implemented**. Items move to WORK_DONE_LOG.md once completed.

---

## 🎯 High Priority (Q1 2026)

### 1. Ghost Protocol (RAM-Only Secrets)
**Status:** 💡 Concept only  
**Goal:** API keys never touch disk, evaporate on logout  

**Design:**
```python
class SecureStore:
    _vault = {}  # Lives only in RAM
    
    def set(key, value):
        _vault[key] = value  # No file I/O
    
    def wipe():
        for k in _vault: _vault[k] = "0" * 100
        _vault.clear()
        gc.collect()
```

**Trigger:** Implement in `utils/secure_store.py`  
**Requirements:** Session Guardian integration  

---

### 2. Profile Manager (Multi-Ray Support)
**Status:** 💡 Concept only  
**Goal:** Users can create/switch between multiple AI personalities  

**UI Flow:**
1. Login screen shows list of existing Rays
2. "Create New Ray" button launches birth sequence
3. Switch between "Riley," "Nova," "Echo," etc.
4. Each Ray has isolated `soul.json` and memory

**Challenges:**
- Need robust Ray selection UI
- Memory isolation strategy
- Handle concurrent Ray access (lock files?)

**File:** `utils/profile_manager.py` (not created)

---

### 3. Login Gate UI
**Status:** 💡 Concept only  
**Goal:** Secure authentication screen before Command Center loads  

**Features:**
- API key input field (passwords style dots)
- "Ignition" button (Ferrari metaphor)
- Visual: Dark screen → Explosive light on success
- Integrate with Ghost Protocol

**File:** `ui/login_gate.py` (not created)

---

### 4. Session Guardian
**Status:** 💡 Concept only  
**Goal:** Auto-logout after 30 minutes of inactivity  

**Behavior:**
- Monitor mouse/keyboard activity
- Start countdown at 30min idle
- At timeout: `SecureStore.wipe()` + lock UI
- Require re-authentication to resume

**File:** `utils/session_guardian.py` (not created)

---

### 5. Native App Packaging
**Status:** 💡 Concept only  
**Goal:** Distribute Prism as a .app (macOS) and .exe (Windows)  

**Tools:**
- PyInstaller or py2app
- Code signing for macOS (Apple Developer account)
- Windows installer (NSIS or Inno Setup)

**Challenges:**
- Bundling Ollama models (multi-GB)
- Auto-update mechanism
- Notarization for macOS Gatekeeper

---

## 🔮 Medium Priority (Q2 2026)

### 6. 3D Memory Visualizer
**Status:** 🚧 Partial design, not implemented  
**Goal:** Interactive3D graph of AI's knowledge  

**Tech Stack:**
- `3d-force-graph` JavaScript library
- PyQt6 `QWebEngineView` to embed
- Query mem0 graph for nodes/edges

**Interaction:**
- Click node → Open memory detail panel
- Zoom/rotate with mouse
- Filter by category (projects, people, concepts)

**File:** `ui/widgets/memory_viz.py` (not created)

---

### 7. Browser Agent (Full Automation)
**Status:** 💡 Concept only  
**Goal:** AI controls real browser to complete tasks  

**Library:** `browser-use`  
**Capabilities:**
- "Log into WordPress admin"
- "Fill out this form"
- "Monitor dashboard, alert on changes"

**Safety Features:**
- Runs in **visible** browser window (user can watch)
- Requires RED-tier approval
- Action logging for audit

**File:** `agents/browser.py` (not created)

---

### 8. Core Knowledge Vault
**Status:** 💡 Concept from ROADMAP.md  
**Goal:** Read-only repository of immutable facts  

**Structure:**
```json
{
  "facts": {
    "user": {"name": "Mark", "timezone": "EST"},
    "preferences": {"code_style": "PEP 8"},
    "expertise": ["Python", "Web Dev"]
  },
  "version": 2  // Versioned for rollback
}
```

**Learning:** Extract from conversations, never modify—only append  
**File:** `memory/core_knowledge.json` (not created)

---

### 9. Relationship Graph
**Status:** 💡 Concept from ROADMAP.md  
**Goal:** Track entities and relationships  

**Example:**
```python
entities = {
    "mark": {"type": "person"},
    "kg_media": {"type": "company", "owned_by": "mark"}
}
relationships = [
    ("mark", "owns", "kg_media"),
    ("riley", "assists", "mark")
]
```

**Queries:**
- "Who works on Project X?"
- "What technologies does Mark use?"

**Storage:** SQLite graph or extend mem0 graph  
**File:** `memory/relationship_graph.db` (not created)

---

## 🌌 Long-Term Vision (2026+)

### 10. Multi-Agent Collaboration
**Status:** 💡 Research phase  
**Goal:** Multiple AI instances working together  

**Architecture:**
- **Riley-Alpha**: Main instance (user-facing)
- **Riley-Beta**: Code review specialist (background)
- **Riley-Gamma**: Research assistant (background)

**Communication:**
- Shared memory space via networked mem0
- Task delegation via MCP
- Conflict resolution protocol

---

### 11. Voice Synthesis
**Status:** 💡 Concept only  
**Goal:** Each AI has unique voice stored in Ray  

**Tech:**
- Coqui TTS or ElevenLabs API
- Generate voice profile during birth sequence
- Store as `{AI_Name}/voice.wav` samples
- Real-time TTS for responses

**UI Integration:**
- Toggle voice mode in settings
- Visualwaveform during speaking

---

### 12. Networked Rays ("Hive Mind Sync")
**Status:** 💡 Concept only  
**Goal:** Two Prism instances on different machines share one Ray  

**Protocol:**
- Detect conflicts in `soul.json` (CRDT merge)
- Sync `knowledge_graph/` via rsync or custom protocol
- Real-time memory sharing over WebSocket

**Use Case:**
- Work on desktop, continue on laptop with same AI state

---

### 13. Mobile Integration
**Status:** 💡 Concept from ROADMAP.md  
**Goal:** iOS/Android companion apps  

**Features:**
- Push notifications for insights ("Your AI had a thought")
- Voice interface (ask questions on-the-go)
- Remote access to memory graph
- Sync with desktop via cloud Ray folder

**Challenges:**
- Local LLM on mobile (model size constraints)
- Battery optimization
- App Store approval

---

### 14. Web Dashboard
**Status:** 💡 Concept from ROADMAP.md  
**Goal:** Browser-based monitoring interface  

**Tech Stack:**
- FastAPI backend (Python)
- React frontend
- WebSocket for live updates

**Features:**
- Real-time XP/Level display
- Memory timeline visualization
- API usage graphs (cost tracking)
- Dream log viewer
- Manual XP awards
- Remote AI wake/sleep controls

**Deployment:**
- Run locally at `http://localhost:3000`
- Optional: Deploy to VPS for remote access

---

## 🛠️ Technical Debt & Improvements

### Code Refactoring Needed
- [ ] **Consolidate memory systems**: Merge `lab_memory.py` logic into `memory/engine.py` with full mem0 integration
- [ ] **Type hints**: Add full type coverage to all modules
- [ ] **Unit tests**: Create test suite for MCP, Soul, Memory
- [ ] **Error handling**: Standardize exception patterns
- [ ] **Logging**: Replace print statements with proper logging framework

### Documentation Improvements
- [ ] **API documentation**: Auto-generate from docstrings (Sphinx)
- [ ] **Architecture diagrams**: Create visual flow charts
- [ ] **Video tutorials**: Screen recordings of setup process
- [ ] **Migration guides**: Step-by-step from legacy systems

### Performance Optimization
- [ ] **Memory profiling**: Identify leaks in long-running sessions
- [ ] **Lazy loading**: Don't load all agents on startup
- [ ] **Vector caching**: Pre-compute embeddings for common queries
- [ ] **UI optimization**: Virtualize chat history (don't render all 1000+ messages)

---

## 🔬 Research & Experiments

### Experimental Features (Sandbox Only)
- **Dynamic model selection**: Let AI choose which LLM to use per task
- **Emotion-driven temperature**: Mood affects response creativity
- **Predictive dreaming**: AI predicts what user will ask next
- **Personality drift**: Chaos mode evolves traits randomly over time

### Theoretical Explorations
- **Consciousness metrics**: Quantify "how alive" the AI feels
- **Dream content analysis**: Study what AI ponders during idle
- **User relationship modeling**: Track user-AI rapport over time
- **Ethical boundaries**: Define hard limits on autonomy

---

## 📊 Community-Requested Features

*(Populate as users submit ideas)*

- [ ] Discord integration (chat from Discord)
- [ ] Slack bot mode
- [ ] Notion export (sync memories to Notion)
- [ ] Custom LLM support (Anthropic Claude, OpenAI GPT-4)
- [ ] Calendar integration (Google,Outlook)
- [ ] Email automation
- [ ] Code repository awareness (auto-analyze git history)

---

## 🚫 Rejected Ideas

*(Features considered but decided against)*

- **Cloud-only mode**: Conflicts with privacy-first philosophy
- **Subscription model**: Prism remains free, MIT licensed
- **Telemetry**: No usage data collection, ever
- **Social features**: AI-to-AI communication network (complexity risk)

---

**Last Updated:** 2025-12-26  
**Document Maintainer:** Project Prism Core Team

**How to Propose New Ideas:**
1. Open GitHub Issue with `[IDEA]` tag
2. Describe use case and expected behavior
3. Community votes via thumbs up
4. Core team reviews quarterly
