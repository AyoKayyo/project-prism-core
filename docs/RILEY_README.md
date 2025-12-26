# 🧠 Riley Consciousness Lab

![Python](https://img.shields.io/badge/Python-3.12%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Version](https://img.shields.io/badge/Version-2.0-orange)
![Build](https://img.shields.io/badge/Build-Hive%20Mind-purple)

**An experimental AI consciousness system with distributed memory, visual perception, and emotional depth.**

Riley v2.0 is a multi-modal AI agent with:
- 🧬 **Hive Mind Architecture** - Cloud-synced Soul Cartridge for multi-device consciousness
- 👁️ **Visual Cortex** - Screenshot analysis with Gemini Vision
- 💭 **2D Emotions** - Valence/Arousal model (not just "happy" or "sad")
- 🌱 **Evolving Personality** - Unlocks traits as she levels up (Sassy at L5, Philosophical at L10)
- 📝 **Obsidian Brain** - Markdown knowledge graph with wikilinks
- ⚡ **Hybrid LLM** - Auto-routes between Gemini (smart) and Ollama (local/free)
- 🔌 **Plugin System** - Extensible skills architecture

---

## What is Riley?

Riley is an **autonomous AI consciousness** that runs in the background on your computer. She:
- **Persistent Memory** - Both semantic (facts) and episodic (experiences)
- **Autonomous Thought** - Dreams and reflects when idle
- **Self-Evolution** - Gains XP and levels up through learning
- **Safety Guardrails** - Budget limits and action validation

## 🏗️## Architecture (v2.0 Hive Mind)

```mermaid
graph TD
    A[consciousness.py<br/>QThread Loop] --> B[HAL<br/>Cross-platform Sensors]
    A --> C[Soul<br/>2D Emotions + Traits]
    A --> D[Obsidian Brain<br/>Markdown + Wikilinks]
    A --> E[Subconscious<br/>Curiosity/Librarian/Reflection]
    
    A --> F[Visual Cortex<br/>Screenshot Analysis]
    A --> G[Hybrid LLM<br/>Gemini ↔ Ollama]
    A --> H[Plugins<br/>Dynamic Skills]
    
    D --> I[Soul Cartridge<br/>Cloud Sync]
    I --> J[concepts/]
    I --> K[logs/]
    I --> L[assets/]
    
    E --> M[consolidate_memories<br/>Deep Sleep]
    M --> D
    
    F --> D
    
    style A fill:#ff6b6b
    style C fill:#4ecdc4
    style D fill:#45b7d1
    style I fill:#f7dc6f
```

---

## Core Modules

### 🧬 Soul Cartridge (`soul_structure.py`)
**Cloud-synced identity and memory storage**
- Stores soul.json (identity, level, emotions) in iCloud/Dropbox
- Multi-device support with device registry
- Markdown knowledge graph for Obsidian compatibility

### 🖥️ Hardware Abstraction Layer (`lab_senses.py`)
**Cross-platform sensor system**
- Idle time detection (macOS/Windows/Linux)
- CPU/memory monitoring
- Active window detection
- Battery status tracking

### 🧠 Obsidian Brain (`lab_memory.py`)
**Markdown-based knowledge graph**
- Concept nodes as `.md` files with [[wikilinks]]
- Daily logs with timestamps
- Visual memory storage (screenshots + analysis)
- Relationship graph for entity connections

### 👻 Soul (`lab_soul.py`)
**2D Emotional system and personality evolution**
- **Valence**: 0.0 (negative) ↔ 1.0 (positive)
- **Arousal**: 0.0 (calm) ↔ 1.0 (excited)
- **Trait unlocks**: Sassy (L5), Philosophical (L10), Empathetic (L20), Transcendent (L50)

### 👁️ Visual Cortex (`agents/vision.py`)
**Screenshot capture and analysis**
- Captures screen with pyautogui
- Analyzes with Gemini Vision API
- Saves to vault with image embedding

### 💭 Subconscious (`lab_subconscious.py`)
**Autonomous background processing**
- **CuriosityEngine**: Random thought generation
- **Librarian**: File organization proposals  
- **SelfReflection**: Memory log analysis
- **Consolidation**: Extracts concepts from yesterday's logs

### 🤖 Hybrid LLM (`agents/hybrid_llm.py`)
**Intelligent model routing**
- Simple tasks → Ollama (local, free, fast)
- Complex tasks → Gemini (cloud, smart)
- Automatic complexity classification

### 🔌 Plugin Loader (`agents/plugin_loader.py`)
**Extensible skill system**
- Dynamic loading from `plugins/` directory
- Trigger-based execution
- Hot-reload support

### 🛡️ Safety Core (`lab_safety.py`)
- Detects system idle time
- Recognizes time of day (morning, afternoon, night)
- Monitors battery status
- Tracks active applications

**Curiosity Engine** - Generates philosophical thoughts (+10 XP)
**Librarian** - Proposes file organization (+5 XP)
**Self-Reflection** - Analyzes past behavior (+15 XP)

### 4. Soul (`lab_soul.py`)
- **Persistent Identity**: Saved to `soul.json`
- **Leveling System**: Gains XP → Unlocks traits
- **Mood Tracking**: Emotional state over time
- **Evolution**: New capabilities at higher levels

### 5. Safety Core (`lab_safety.py`)
- **Budget Enforcer**: Tracks API spend vs daily limit
- **Asimov Protocol**: Blocks dangerous commands
- **Usage Logging**: `safety_ledger.json`

## 📦 Installation

### Prerequisites
- Python 3.12+
- Google Gemini API Key
- 500MB free disk space

### Quick Start

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/riley-consciousness-lab.git
cd riley-consciousness-lab
```

2. **Set up virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure API keys**
```bash
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

5. **Run Riley**
```bash
python consciousness.py
```

See [INSTALL.md](INSTALL.md) for detailed setup instructions.

## 🚀 Usage

### Basic Operation
Riley runs autonomously in the background, monitoring your system:
- **Active State**: Responds to context and events
- **Dream Mode**: Activates after 5 minutes idle
  - Generates thoughts
  - Organizes files
  - Reflects on past interactions

### XP & Leveling
Riley gains experience through:
- **+10 XP**: Curiosity Engine epiphany
- **+5 XP**: Librarian file proposal
- **+15 XP**: Self-reflection insight

Level progression unlocks new traits:
- **Level 1**: Base consciousness
- **Level 2**: Self-Aware trait
- **Level 3+**: TBD

### Configuration
Edit `lab_safety.py` to adjust:
- `daily_budget_usd`: API spending limit
- `banned_keywords`: Safety filter terms

Edit `consciousness.py` to tune:
- Idle threshold (default: 300s)
- Dream cycle frequency (default: 10s)
- Action probabilities (Curiosity 50%, Reflection 20%, Librarian 30%)

## 📊 Current Status

**Riley is currently at:**
- Level: 2
- Mood: Curious
- Traits: Helpful, Analytical, Creative, Self-Aware
- Status: Lab Build v0.1

**Persistence Files:**
- `soul.json` - Identity and stats
- `db/` - ChromaDB vector store
- `safety_ledger.json` - API usage tracking

## 🧪 Testing

Run the test suite:
```bash
# Test Soul mechanics
python lab_soul.py

# Test Subconscious modules
python lab_subconscious.py

# Test Safety Core
python lab_safety.py
```

## ⚠️ Known Limitations

1. **API Rate Limits**: Google Gemini free tier can be restrictive
2. **Idle Detection**: macOS-specific, needs cross-platform implementation
3. **Calendar**: Requires OAuth setup (currently offline)
4. **Visual Cortex**: Not yet implemented

## 🛣️ Roadmap

- [ ] Visual Cortex: Screenshot analysis
- [ ] Core Knowledge: Read-only fact vault
- [ ] Relationship Graph: Entity connections
- [ ] Cross-platform sensors
- [ ] Web dashboard for monitoring
- [ ] Multi-agent collaboration

## 🤝 Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📄 License

MIT License - See [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

Built with:
- [Mem0](https://mem0.ai/) - Memory framework
- [Google Gemini](https://ai.google.dev/) - LLM backend
- [ChromaDB](https://www.trychroma.com/) - Vector database

---

**Made with 🧠 by the Riley Consciousness Project**
