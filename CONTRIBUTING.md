# Contributing to Project Prism

Thank you for your interest in contributing! 🎉

## Code of Conduct

- **Privacy first** - Never compromise user data
- **Safety first** - All destructive actions require approval
- **No hardcoding** - Dynamic naming, no assumptions
- **Local preference** - Cloud only when necessary

## Getting Started

1. Fork the repository
2. Create a feature branch: `git checkout -b feature /awesome-feature`
3. Read `DEV_INSTRUCTIONS.md` for coding standards
4. Make your changes
5. Test thoroughly
6. Commit: `git commit -m "Add awesome feature"`
7. Push: `git push origin feature/awesome-feature`
8. Open a Pull Request

## Development Setup

```bash
git clone https://github.com/AyoKayyo/project-prism-core.git
cd project-prism-core
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## What to Work On

Check [IDEAS_BACKLOG.md](IDEAS_BACKLOG.md) for planned features:

**High Priority:**
- UI components (Command Center, Login Gate)
- Ollama/Gemini LLM integration
- mem0 deep memory integration
- Browser automation agent

**Medium Priority:**
- 3D Memory Visualizer
- Voice synthesis
- Additional agents (Coder, Architect, Researcher)

## Testing

```bash
# Run unit tests (when available)
pytest

# Manual testing
python core/main.py
```

## Pull Request Guidelines

- **One feature per PR**
- **Update WORK_DONE_LOG.md** if adding implemented features
- **Add to IDEAS_BACKLOG.md** if proposing new features
- **Follow naming conventions** (no hardcoded "Riley")
- **Respect MCP safety tiers** for new actions
- **Add docstrings** to all functions

## Architecture Rules

1. **No hardcoded AI names** - Use `soul.get_name()`
2. **No disk secrets** - Use `SecureStore` (Ghost Protocol)
3. **All actions through MCP** - Safety evaluation required
4. **Dynamic imports** - Don't break if optional deps missing

## Questions?

- Open a GitHub Issue
- Check `DEV_INSTRUCTIONS.md`
- Review `ARCHITECTURE_SPEC.md`

---

**Thank you for helping build the future of personal AI!** 💎
