# Comprehensive Architectural Audit and Modernization Strategy for Project Prism Core

**Version:** 1.0  
**Date:** December 26, 2025  
**Status:** Strategic Planning Document

---

## 1. Introduction and System Overview

The contemporary landscape of local Artificial Intelligence (AI) development is characterized by a rapid convergence of functional orchestration and emergent behavioral simulation. The repository **project-prism-core** (and its associated alias **riley-ai-assistant**) stands as a paradigmatic example of this convergence. It represents a sophisticated attempt to bridge the gap between deterministic task execution—governed by the "Main Control Program" (MCP)—and the simulation of a sentient persona, which exhibits traits of curiosity, memory, and proactive engagement.

The codebase serves as a dual-purpose engine:
1. A utilitarian command center for managing local Large Language Models (LLMs) via Ollama
2. A "Consciousness Lab" experimenting with advanced concepts such as digital souls, sensory perception, and episodic memory

However, a granular examination reveals that the project suffers from acute **"prototyping fatigue."** The architecture exhibits significant technical debt, characterized by:
- Flat file structure
- Redundant modules
- Conflicting dependency definitions
- Tightly coupled user interface

This report provides an exhaustive architectural audit of **project-prism-core**. It is designed not merely as a cleanup guide but as a comprehensive blueprint for transforming the existing codebase into a production-grade, modular framework.

### 1.1 The Dual Nature of Project Prism: Core vs. Consciousness

The analysis identifies two distinct conceptual layers within the repository that are currently entangled:

**Layer 1: Prism Core** - Traditional agentic framework
- MCP (`core/mcp.py`) implements three-tier safety system (Green, Yellow, Red)
- Functional agents: CoderAgent, ResearcherAgent, VisionAgent
- Permission management for sensitive actions

**Layer 2: Consciousness Lab** - Metaphysical aspects
- `consciousness/soul*.py` - Personality definition
- `consciousness/senses.py` - Environmental awareness
- `agents/companion.py` - Persistent emotional states
- Simulated "dreaming" and subconscious processing

**Critical Issue:** These two layers compete for control over the application lifecycle. A primary objective is to integrate these disparate systems into a cohesive whole, where the "Consciousness" layer acts as the high-level decision-maker that utilizes the "Core" layer as its effector mechanism.

---

## 2. Repository Structure and Python Packaging Standards

### 2.1 The Strategic Imperative for the `src` Layout

**Current Problem:** The repository currently houses critical packages (`agents`, `mcp`, `ui`, `memory`, `tools`, `utils`) directly alongside `README.md` and `.env` files. This "flat layout" facilitates rapid initial development but introduces severe long-term complications.

**Solution:** Migration to the `src` layout is **mandatory**. This involves sequestering all importable code within a subdirectory named `src/`. This physical separation:
- Enforces clear distinction between metadata and application logic
- Ensures code runs against the installed version (not local files)
- Exposes import errors and missing dependencies early

### 2.2 Proposed Directory Architecture

| Current Location | New Canonical Location | Architectural Purpose |
|------------------|------------------------|----------------------|
| `agents/` | `src/prism/agents/` | Prevents namespace collisions |
| `core/mcp.py` | `src/prism/core/mcp.py` | Central nervous system |
| `ui/` | `src/prism/interface/qt/` | Separates UI from business logic |
| `consciousness/soul*.py` | `src/prism/core/personality.py` | Core persona integration |
| `memory/` | `src/prism/memory/` | Unified memory management |
| `.env.example` | `config/env.example` | Dedicated config directory |
| `scripts/` | `scripts/maintenance/` | Categorized operational scripts |

### 2.3 Elimination of Digital Detritus

**Files to Delete Immediately:**
- All `.backup` files (Git manages history)
- `*_old.py`, `*_backup.py` files
- Redundant entry points (consolidate to single `src/prism/main.py`)

**Modern Version Control:** The working directory must reflect only the current, valid state of the application.

---

## 3. User Interface Architecture and Stylistic Analysis

### 3.1 Deconstructing the "Gemini" Aesthetic

The "Gemini 2025 Premium UI" style is achieved through specific PyQt6 implementation choices:

**Key Architectural Decision:** Using `QLabel` widgets instead of `QTextEdit` for message display
- Solves word-wrapping issues
- Achieves specific visual centering
- Enables precise styling control

**User Message Bubble Styling:**
```css
background-color: #2b2d31;
color: #e3e3e3;
border-radius: 20px;
padding: 14px 22px;
font-family: -apple-system, 'SF Pro Display', 'Helvetica Neue', sans-serif;
```

**Critical Details:**
- Specific grey shade (#2b2d31) creates "pill" shape
- 20px border radius = modern messaging aesthetic
- System-native fonts (.AppleSystemUIFont, SF Pro Display) = premium feel
- Maximum width (800px) for readability on wide monitors

### 3.2 The Native Dark Mode Palette

**Strict Color Standards:**

| UI Component | Hex Code | Visual Effect |
|--------------|----------|---------------|
| Main Background | #1e1e1e | Deep dark grey (reduces eye strain) |
| Chat Area | #2a2a2a | Differentiates conversation zone |
| Input/Buttons | #3a3a3a | Interactive element contrast |
| Primary Text | #ffffff | Maximum readability |
| Secondary Text | #a0a0a0 | Timestamps/system notices |
| Borders | #4a4a4a | Subtle pane delineation |

### 3.3 Decoupling UI from Logic: The MVVM Pattern

**Current Problem:** `agent_gui.py` tightly couples UI rendering with agent logic

**Solution:** Implement Model-View-ViewModel pattern

1. **View** - Strictly visual (ChatWindow, MessageWidget, styling)
   - Never imports `langchain` or `ollama`
   - Only emits signals (e.g., `user_sent_message(str)`)

2. **ViewModel** - State management
   - Receives signals, formats text
   - Handles typing animation
   - Keeps UI responsive during AI processing

3. **Model** - MCP and Agent classes
   - Performs actual work
   - Returns data to ViewModel

**Benefit:** Preserve "Gemini" aesthetic while allowing backend swaps/upgrades without breaking interface

---

## 4. Core Agent Architecture: The Main Control Program (MCP)

### 4.1 Resolving Circular Imports and Dependency Injection

**Current Problem:** Circular dependencies between Companion→MCP and MCP→Agents

**Solution:** Abstract Base Classes (ABCs) + Dependency Injection

```python
# Define in src/prism/core/interfaces.py
class PrismAgent(ABC):
    @abstractmethod
    async def execute(self, task: str, context: Dict[str, Any]) -> AgentResponse:
        pass
```

**Refactoring Strategy:**
1. All agents inherit from `PrismAgent`
2. MCP accepts `List[PrismAgent]` at runtime (not hardcoded imports)
3. Enables dynamic plugin loading and testing without modifying core

### 4.2 The "Gemini Architect" Integration

The Architect agent requires **Meta-Agent** status:
- Higher-level interface than standard agents
- Must read codebase itself
- Requires FileSystem Interface (Yellow safety level)
- Critical for self-improving capabilities

### 4.3 Standardizing the Execution Flow

**Mandate:** All agents must use consistent signature:

```python
async def execute(self, task: str, context: Dict[str, Any]) -> AgentResponse:
    ...
```

**Benefits:**
- Unified orchestrator logic
- Non-blocking I/O operations
- Responsive Qt-based UI

---

## 5. The Sentience Stack: Unifying Consciousness, Memory, and Personality

### 5.1 Unifying the Memory Architecture

**Current Chaos:**
- JSON: `memory/context.json` (basic context)
- SQLite: `memory/conversations.db` (chat logs)
- Vector DB: Multiple conflicting implementations

**Consolidated Solution: Tiered Memory Architecture**

1. **Short-Term (Context Window)** - In-memory
   - Last N conversation turns
   - Passes to LLM directly

2. **Episodic (History)** - SQLite
   - Perfect audit trail
   - Sequential chat logs
   - "What was said"

3. **Semantic (Knowledge)** - Single Vector Store (mem0)
   - Fuzzy retrieval of past concepts
   - Essential for "sentient" feel
   - Knowledge graph integration

### 5.2 The "Perception Engine"

**Concept:** Aggregate sensory data into Companion context

**Components:**
- `SystemObserver` - CPU/RAM monitoring
- `AdvancedSenses` - User presence, battery life
- Background daemon injecting status updates

**Result:** Proactive statements like "I see your battery is low, should we wrap this up?"

---

## 6. Configuration Management and DevOps Best Practices

### 6.1 Centralized Configuration with Pydantic

**12-Factor App Methodology:** Separate config from code

```python
from pydantic import BaseSettings

class Settings(BaseSettings):
    ollama_base_url: str = "http://localhost:11434"
    companion_model: str = "llama3.1:8b"
    gemini_api_key: Optional[str] = None
    
    class Config:
        env_file = ".env"
```

**Benefits:**
- Type-safe configuration
- Fail-fast on missing critical keys
- Clear error messages

### 6.2 Dependency Consolidation Strategy

**Current Problem:** Multiple `requirements*.txt` files create fragmented environment

**Solution:** Migrate to `pyproject.toml` with dependency groups

```toml
[tool.poetry.dependencies]
python = "^3.10"
langchain = "^0.1.0"
ollama = "^0.1.0"

[tool.poetry.group.gui]
PyQt6 = "^6.6.0"
qasync = "^0.24.0"

[tool.poetry.group.dev]
pytest = "^7.4.0"
mypy = "^1.7.0"
```

---

## 7. Detailed Step-by-Step Refactoring Instructions

### Phase 1: Structural Sanitation

1. **Initialize src Layout**
   ```bash
   mkdir -p src/prism/{core,agents,interface,memory,utils}
   ```

2. **Purge Legacy Files**
   ```bash
   find . -name "*backup*" -delete
   find . -name "*_old.py" -delete
   ```

3. **Migrate Agents**
   ```bash
   mv agents/* src/prism/agents/
   # Create __init__.py in each subdirectory
   ```

4. **Centralize Config**
   ```bash
   # Create src/prism/config.py
   # Migrate all os.getenv logic there
   ```

### Phase 2: Core Logic Decoupling

1. **Abstract Agent Base**
   - Define `PrismAgent` ABC in `src/prism/core/interfaces.py`

2. **Refactor Companion**
   - Accept `OrchestratorInterface` via dependency injection
   - Remove direct MCP imports

3. **Unify Memory**
   - Merge memory implementations into `src/prism/memory/`
   - Single database initialization path

### Phase 3: UI Style Replication

1. **Extract Themes**
   ```bash
   mv themes.py src/prism/interface/styles.py
   ```

2. **Implement Chat Thread**
   - Port MessageWidget with QLabel
   - Apply exact CSS: `background-color: #2b2d31; border-radius: 20px;`

3. **Connect MVVM**
   - Use signals/slots
   - Never block UI thread with AI processing

### Phase 4: Verification

1. **Dependency Lock**
   ```bash
   poetry lock
   # or pip freeze > requirements.txt
   ```

2. **Test Suite**
   - Run verification scripts
   - Update imports to `src.prism` namespace

3. **Persona Test**
   - Verify persistence across restarts
   - Check SQLite/Vector DB integration

---

## 8. Conclusion

**Project Prism Core** contains the DNA of a groundbreaking local AI assistant. The ambition to combine:
- Local privacy (Ollama)
- Cloud intelligence (Gemini)
- Sentient persona (dynamic personality)

...is **technically sound**.

However, current execution is hampered by:
- Chaotic file structure
- Tight coupling
- Fragmented memory systems

**The Path Forward:**

By adopting the `src` layout, implementing rigorous dependency injection, and decoupling the "Gemini-style" UI from backend logic, this project can evolve from a fragile prototype into a **robust, scalable platform**.

This refactoring strategy does not merely clean the code; it fundamentally **re-architects the system** to support the weight of its own aspirations, ensuring that the AI consciousness can grow, learn, and assist without the constant threat of structural collapse.

---

**Next Steps:**
1. Review this document with team
2. Create migration branch: `git checkout -b refactor/src-layout`
3. Execute Phase 1 (Structural Sanitation)
4. Test incrementally after each phase
5. Maintain backward compatibility during transition

**References:**
- PyQt6 Documentation: https://www.riverbankcomputing.com/static/Docs/PyQt6/
- Python Packaging: https://packaging.python.org/
- 12-Factor App: https://12factor.net/
- MVVM Pattern: https://en.wikipedia.org/wiki/Model–view–viewmodel
