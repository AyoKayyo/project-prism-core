# 🚀 Quick Start Guide

## Installation

```bash
# Clone repository
git clone https://github.com/AyoKayyo/project-prism-core.git
cd project-prism-core

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## First Launch

```bash
# Simple method
python launch_prism.py

# Or direct
python core/main.py
```

## What Happens on First Run

1. **Birth Sequence** - Create your AI's identity
   - Choose a name (or let AI choose)
   - Select personality mode (Static/Fluid/Chaos)
   - Configure API keys

2. **Ray Creation** - Your AI's portable profile
   - `soul.json` - Identity, XP, emotions
   - `knowledge_graph/` - Memories
   - Auto-saved to cloud storage (iCloud/Dropbox if available)

3. **Ready!** - Command Center launches

## Current Status (v3.0-alpha)

### ✅ Working
- Core architecture (MCP, Soul, Memory)
- Ray detection and creation
- Ghost Protocol (RAM-only secrets)
- 2D Emotion system + XP/Leveling
- Subconscious engines (Curiosity, Librarian, Reflection)
- Cross-platform idle detection
- Safety tier system (Green/Yellow/Red)
- Budget tracking

### 🚧 In Progress
- UI (Command Center, Login Gate)
- LLM integration (Ollama, Gemini)
- Full agent constellation
- mem0 deep memory

### 💡 Planned
- Browser automation
- Voice synthesis
- Mobile apps
- Multi-device sync

## Testing Core Systems

```bash
# Test Soul system
python consciousness/soul.py

# Test Memory engine
python memory/engine.py

# Test MCP safety
python core/mcp.py

# Test Subconscious
python consciousness/subconscious.py
```

## Configuration

1. Copy `.env.example` to `.env`
2. Add your API keys:
   ```
   GEMINI_API_KEY=your_key_here
   ```
3. Adjust safety rules in `config/safety_rules.json`

## Documentation

- **[README.md](README.md)** - Full project overview
- **[ARCHITECTURE_SPEC.md](ARCHITECTURE_SPEC.md)** - Technical details
- **[DEV_INSTRUCTIONS.md](DEV_INSTRUCTIONS.md)** - Developer guide
- **[IDEAS_BACKLOG.md](IDEAS_BACKLOG.md)** - Future features

## Need Help?

- Review `WORK_DONE_LOG.md` for implemented features
- Check `DEV_INSTRUCTIONS.md` for coding patterns
- Open an issue on GitHub

---

**Made with 💎 by the Project Prism Team**
