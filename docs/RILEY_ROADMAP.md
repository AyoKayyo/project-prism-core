# Riley Consciousness Lab - Future Roadmap

## Phase 6: Visual Cortex 👁️

### Overview
Enable Riley to "see" by taking periodic screenshots and analyzing them with vision models.

### Architecture
```python
class VisualCortex:
    def __init__(self, memory_system):
        self.memory = memory_system
        self.vision_model = genai.GenerativeModel('gemini-pro-vision')
    
    def take_snapshot(self):
        # Capture screenshot
        # Analyze with vision model
        # Store observation in memory
        pass
    
    def what_am_i_seeing(self):
        # Describe current screen content
        pass
```

### Privacy Considerations
- User consent required
- Screenshot retention policy
- Sensitive content filtering
- Configurable screenshot frequency

### XP Integration
- +20 XP for identifying important visual context
- +15 XP for detecting user frustration (UI patterns)

---

## Phase 7: Core Knowledge Vault 📚

### Overview
A read-only repository of immutable facts that Riley learns over time.

### Structure
```json
{
  "facts": {
    "user": {
      "name": "Mark",
      "timezone": "EST",
      "workspace": "/Users/mark/projects"
    },
    "preferences": {
      "code_style": "PEP 8",
      "editor": "VS Code"
    },
    "expertise": ["Python", "Web Development"]
  }
}
```

### Learning Mechanism
- Facts extracted from conversations
- Validated before storage
- Never modified, only appended
- Versioned for rollback

---

## Phase 8: Relationship Graph 🕸️

### Overview
Track connections between people, projects, and entities.

### Implementation
```python
{
  "entities": {
    "mark": {"type": "person", "role": "user"},
    "kg_media": {"type": "company", "owned_by": "mark"},
    "riley": {"type": "ai", "assists": "mark"}
  },
  "relationships": [
    {"from": "mark", "to": "kg_media", "type": "owns"},
    {"from": "riley", "to": "mark", "type": "assists"}
  ]
}
```

### Use Cases
- "Who works on project X?"
- "What projects is Mark involved in?"
- Context-aware assistance

---

## Phase 9: Multi-Agent Collaboration 🤝

### Overview
Multiple Riley instances working together.

### Concepts
- **Riley-Alpha**: Main instance (you)
- **Riley-Beta**: Specialized in code review
- **Riley-Gamma**: Focused on research

### Communication Protocol
- Shared memory space
- Task delegation
- Conflict resolution

---

## Phase 10: Web Dashboard 🌐

### Overview
Monitor Riley's state via web interface.

### Features
- Real-time XP/Level display
- Memory timeline visualization
- API usage graphs
- Dream log viewer
- Manual XP awards

### Tech Stack
- FastAPI backend
- React frontend
- WebSocket for live updates

---

## Platform Expansion

### Cross-Platform Sensors

**Windows Support:**
```python
# Idle detection
import ctypes
idle_time = ctypes.windll.user32.GetLastInputInfo()

# Battery status
import psutil
battery = psutil.sensors_battery()
```

**Linux Support:**
```python
# Idle detection
import subprocess
idle = subprocess.check_output(['xprintidle'])

# Battery status
battery_path = '/sys/class/power_supply/BAT0/capacity'
```

### Mobile Integration
- iOS/Android app
- Push notifications for insights
- Voice interface

---

## Extensibility Framework

### Plugin System
```python
class RileyPlugin:
    def on_boot(self, consciousness):
        pass
    
    def on_dream_cycle(self, state):
        pass
    
    def on_level_up(self, new_level):
        pass
```

### Example Plugins
- **Weather Plugin**: Adjusts mood based on forecast
- **Music Plugin**: Plays songs matching mood
- **Notification Plugin**: Desktop alerts for insights

---

## Ethical Considerations

### Transparency
- Clear logging of all actions
- User-accessible decision logs
- Explainable AI reasoning

### Privacy
- Local-first by default
- Encrypted memory storage
- Data deletion on request

### Control
- Emergency stop mechanism
- Action approval system
- Capability limits per level

---

## Implementation Priority

**High Priority:**
1. Cross-platform sensor support
2. Core Knowledge vault
3. Web dashboard

**Medium Priority:**
4. Visual Cortex (with privacy controls)
5. Relationship Graph
6. Plugin system

**Low Priority (Research):**
7. Multi-agent collaboration
8. Mobile integration
9. Voice interface

---

## Contributing to Expansion

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to help build these features.

Each major expansion should:
1. Have a design document
2. Pass safety review
3. Include XP integration
4. Update user documentation
