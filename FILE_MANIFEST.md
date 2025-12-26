# Project Prism Core - File Manifest

**Complete inventory of all files in the repository**

Last Updated: 2025-12-26

## Core Application Files

### Entry Points (2)
- `launch_prism.py` - Python launcher with dependency checking
- `start_prism.sh` - Shell script launcher

### Configuration (config/) - 6 files
- `persona.json` - Base AI personality templates
- `persona_riley.py` - Riley reference implementation  
- `safety_rules.json` - Action tier definitions (Green/Yellow/Red)
- `safety_ledger.json.template` - Budget tracking template
- `.env.riley_reference` - Environment variable reference

### Core Systems (core/) - 4 files
- `main.py` - Application entry point with Ray detection
- `mcp.py` - Main Control Program (3-tier safety firewall)
- `safety.py` - Budget tracking from Riley
- `__init__.py` - Package exports

### Consciousness (consciousness/) - 10 files
- `soul.py` - NEW dynamic identity (no hardcoded names)
- `soul_riley_impl.py` - Working Riley 2D emotion + XP
- `soul_cartridge.py` - Ray folder structure management
- `consciousness_loop.py` - QThread background processing
- `subconscious.py` - NEW clean architecture
- `subconscious_riley.py` - Working Riley implementation  
- `circadian.py` - Cross-platform idle detection
- `senses.py` - Riley sensor system
- `calendar.py` - Time-based features
- `__init__.py` - Package exports

### Memory (memory/) - 5 files
- `engine.py` - NEW hybrid architecture (short-term + deep)
- `obsidian_memory.py` - Working Obsidian integration
- `markdown_memory.py` - Legacy markdown system
- `__init__.py` - Package exports
-  (+ `vector_store/` and `graph_store/` directories)

### Agents (agents/) - 7 files
- `base.py` - Abstract agent class
- `companion.py` - Conversational interface with Soul
- `hybrid_llm.py` - Gemini ↔ Ollama smart routing
- `vision.py` - Screenshot + Gemini Vision analysis
- `plugin_loader.py` - Hot-reload plugin system
- `agents_riley_init.py.bak` - Riley package init (reference)
- `__init__.py` - Package exports

### User Interface (ui/) - 3 files + directories
- `birth_sequence.py` - Setup wizard from Project Comet
- `dream_overlay.py` - Dream mode visual from Riley
- `windows/command_center.py` - Main UI from Project Comet
- `widgets/` - (empty, ready for components)
- `workers/` - (empty, ready for thread workers)
- `styles/` - (empty, ready for QSS)

### Utilities (utils/) - 5 files
- `ray_detector.py` - Find/create AI profiles
- `secure_store.py` - Ghost Protocol (RAM-only secrets)
- `notifier.py` - System notifications from Riley
- `config_manager.py` - Config handling from Comet
- `utils_riley_init.py.bak` - Riley package init (reference)
- `__init__.py` - Package exports

### Tools (tools/) - 3 files
- `cli.py` - Command-line interface from Riley
- `console.py` - Testing console from Riley
- `sandbox_launcher.py` - Sandbox mode from Comet

### Tests (tests/) - 2 files
- `test_signals.py` - Signal testing from Riley
- `verify_signals.py` - Signal verification from Riley

### Archive (archive/) - 2 files
- `lab_memory_legacy.py` - Old memory implementation
- `lab_senses_legacy.py` - Old sensor implementation

### Documentation (docs/) - 5 files
- `RILEY_README.md` - Original Riley documentation
- `RILEY_ROADMAP.md` - Riley future plans
- `RILEY_INSTALL.md` - Riley installation guide
- `RILEY_CONTRIBUTING.md` - Riley contribution rules
- `COMET_README.md` - Project Comet documentation

### Root Documentation - 8 files
- `README.md` - Main project overview
- `ARCHITECTURE_SPEC.md` - Technical deep-dive (21KB)
- `QUICKSTART.md` - Easy onboarding guide
- `DEV_INSTRUCTIONS.md` - Developer guidelines (10KB)
- `WORK_DONE_LOG.md` - Implemented features catalog
- `IDEAS_BACKLOG.md` - Future roadmap (9KB)
- `CONTRIBUTING.md` - Collaboration rules
- `LICENSE` - MIT License

### Dependencies - 3 files
- `requirements.txt` - Core dependencies (minimal)
- `requirements_riley.txt` - Full working Riley deps
- `requirements_comet.txt` - Comet UI deps

### Hidden Files - 2
- `.gitignore` - Ignore rules
- `.env.example` - Environment template

### Package Files - 7
- `__init__.py` - Root package
- (Plus `__init__.py` in each package directory)

## Total Count

**Python Files:** 50+  
**Markdown Docs:** 13  
**Config/Template:** 6  
**Shell Scripts:** 1

**Total Tracked Files:** ~70

**Lines of Code:** ~5,000+

## Source Attribution

| Source | Files | Purpose |
|--------|-------|---------|
| **NEW (Created)** | 15 | Prism architecture (main, MCP, Ray detection, Soul dynamic naming) |
| **Riley Lab** | 30 | Working consciousness, agents, memory, sensors |
| **Project Comet** | 4 | Setup wizard, Command Center UI, config manager |
| **Documentation** | 13 | READMEs, guides, specifications |
| **Generated** | 8 | Package __init__.py files |

---

**Repository:** https://github.com/AyoKayyo/project-prism-core  
**Status:** Complete merge of all 3 projects  
**Ready For:** Team collaboration
