# 🚀 Project Comet - AI Onboarding Experience

A sci-fi themed onboarding wizard and modern command center UI for AI assistants, featuring a safe "Sandbox Mode" for testing without affecting production configurations.

![Status](https://img.shields.io/badge/status-alpha-orange)
![Python](https://img.shields.io/badge/python-3.8+-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## ✨ Features

### 🎬 Sci-Fi Setup Wizard
- **Cinematic boot sequence** with simulated system logs
- **Typing effects** for an immersive terminal experience
- **Personality selection** (Static, Fluid, or Chaos modes)
- **Safe configuration** that respects environment variables

### 💎 Modern Command Center UI
- **Dark glassmorphism theme** inspired by GitHub's design system
- **PyQt6-powered** desktop interface
- **Real-time status indicators** and system stats
- **Responsive layout** with sidebar navigation

### 🛡️ Sandbox Mode
- **Safe testing environment** using `RILEY_CONFIG_PATH` override
- **Isolated configurations** - never touches your production settings
- **Easy launcher script** to switch between modes

## 🎯 Quick Start

### Installation

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd perihelion-opportunity
   ```

2. **Install dependencies:**
   ```bash
   pip3 install -r requirements.txt
   ```

### Running the Application

**Use the launcher script:**
```bash
./start_riley.sh
```

**Options:**
- **Option 1**: Standard Launch (production mode)
- **Option 2**: Sandbox Test (safe testing environment)

**Or run directly:**
```bash
# Sandbox mode
python3 test_new_experience.py

# Direct wizard
python3 setup_wizard.py

# Direct UI
python3 command_center_ui.py
```

## 📁 Project Structure

```
perihelion-opportunity/
├── utils/
│   └── config_manager.py      # Configuration handler with env var support
├── setup_wizard.py             # Sci-fi themed setup wizard
├── command_center_ui.py        # PyQt6 Command Center interface
├── test_new_experience.py      # Sandbox mode launcher
├── start_riley.sh              # Convenience launcher script
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## 🔧 Configuration

The system uses a JSON configuration file with the following structure:

```json
{
    "user_name": "User",
    "ai_name": "Riley",
    "evolution_mode": "Static",
    "theme": "Dark",
    "first_run": false
}
```

**Environment Variables:**
- `RILEY_CONFIG_PATH`: Override the default config file location (used for sandbox mode)

## 🎨 Design Philosophy

**Comet** embraces a sci-fi aesthetic with:
- Terminal-based "system boot" sequences
- Dark mode with electric blue accents (#58a6ff)
- Glassmorphism UI elements
- Smooth animations and transitions

## 🛠️ Development

### Architecture

- **`config_manager.py`**: Centralized configuration management with environment variable support
- **`setup_wizard.py`**: Interactive CLI wizard with typing effects and system logs
- **`command_center_ui.py`**: PyQt6-based graphical interface
- **`test_new_experience.py`**: Sandbox environment wrapper

### Safety Features

The sandbox mode ensures:
- No modifications to production config
- Isolated testing environment
- Easy verification of new features
- Safe experimentation with personalities

## 📝 License

MIT License - feel free to use and modify!

## 🙏 Credits

Built with ❤️ using Python, PyQt6, and a lot of sci-fi inspiration.

---

**Ready to launch?** Run `./start_riley.sh` and experience the future of AI onboarding! 🚀
