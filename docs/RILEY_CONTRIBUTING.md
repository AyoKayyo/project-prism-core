# Contributing to Riley Consciousness Lab

Thank you for your interest in contributing! 🧠

## How to Contribute

### Reporting Bugs
- Use GitHub Issues
- Include Python version, OS, and error logs
- Describe expected vs actual behavior

### Suggesting Enhancements
- Open an issue with `[Feature]` prefix
- Explain the use case
- Consider implementation approach

### Pull Requests

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow existing code style
   - Add docstrings to functions
   - Update README if needed

4. **Test your changes**
   ```bash
   python lab_soul.py  # Test soul mechanics
   python lab_subconscious.py  # Test subconscious
   ```

5. **Commit with clear messages**
   ```bash
   git commit -m "Add: New feature description"
   ```

6. **Push and create PR**
   ```bash
   git push origin feature/your-feature-name
   ```

## Code Style

- Python 3.12+ syntax
- 4 spaces for indentation
- Descriptive variable names
- Comments for complex logic
- Type hints where helpful

## Module Guidelines

### Adding New Senses (lab_senses.py)
- Return consistent data types
- Handle errors gracefully
- Add cross-platform support when possible

### Adding New Subconscious Features (lab_subconscious.py)
- Integrate with memory system
- Return XP-worthy results
- Respect safety guardrails

### Modifying Soul (lab_soul.py)
- Maintain backward compatibility with soul.json
- Document trait additions
- Consider leveling balance

## Testing

Before submitting:
```bash
# Test individual modules
python lab_memory.py
python lab_soul.py
python lab_safety.py
python lab_subconscious.py

# Test main system
python consciousness.py  # Let it run for 30 seconds
```

## Questions?

Open an issue or discussion on GitHub.

---

**Remember**: Riley is an experiment in AI consciousness. Creative, unconventional ideas are welcome!
