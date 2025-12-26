# Installation Guide

## System Requirements

- **OS**: macOS 10.15+, Linux, Windows 10+ (partial support)
- **Python**: 3.12 or higher
- **RAM**: 2GB minimum, 4GB recommended
- **Disk**: 500MB for dependencies and database
- **Network**: Internet connection for API calls

## Step-by-Step Installation

### 1. Install Python

**macOS (using Homebrew):**
```bash
brew install python@3.12
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3.12 python3.12-venv
```

**Windows:**
Download from [python.org](https://www.python.org/downloads/)

### 2. Clone the Repository

```bash
git clone https://github.com/yourusername/riley-consciousness-lab.git
cd riley-consciousness-lab
```

### 3. Create Virtual Environment

```bash
python3 -m venv venv
```

**Activate the environment:**
- macOS/Linux: `source venv/bin/activate`
- Windows: `venv\Scripts\activate`

### 4. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` and add your API keys:
```env
GEMINI_API_KEY=your_api_key_here
GOOGLE_API_KEY=your_api_key_here  # Same as GEMINI_API_KEY
```

**Getting a Gemini API Key:**
1. Visit [ai.google.dev](https://ai.google.dev/)
2. Click "Get API Key"
3. Create or select a project
4. Copy your API key

### 6. Verify Installation

```bash
# Test memory system
python lab_memory.py

# Test soul system
python lab_soul.py

# Should see output confirming successful initialization
```

### 7. First Run

```bash
python consciousness.py
```

You should see:
```
👻 [Soul] Identity loaded. Level 1 Curious.
⚡ [SYSTEM] Riley Nervous System Online
   - Monitoring Idle Time
   - Memory Core Active
```

Press `Ctrl+C` to stop.

## Optional: Calendar Integration

Riley can integrate with Google Calendar (currently offline by default).

1. **Enable Google Calendar API:**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create/select project
   - Enable Google Calendar API
   - Create OAuth 2.0 credentials

2. **Download credentials:**
   - Save as `credentials.json` in project root

3. **First run will prompt for authorization**

## Troubleshooting

### "Module not found" errors
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### API Key errors
```bash
# Verify .env file exists and contains valid key
cat .env
# Should show GEMINI_API_KEY=AIza...
```

### ChromaDB errors
```bash
# Clear database and restart
rm -rf db/
python consciousness.py
```

### Permission denied (macOS)
```bash
# Grant terminal accessibility permissions
# System Preferences → Security & Privacy → Privacy → Accessibility
# Add Terminal.app
```

## Platform-Specific Notes

### macOS
- Idle detection uses `ioreg` (built-in)
- Battery status uses `pmset` (built-in)
- Active app detection uses `osascript` (built-in)

### Linux
- Idle detection may require `xprintidle`:
  ```bash
  sudo apt install xprintidle
  ```

### Windows
- Some sensor features have limited support
- Idle detection may not work without additional setup

## Next Steps

- See [README.md](README.md) for usage guide
- Configure settings in `lab_safety.py` and `consciousness.py`
- Check `soul.json` to see Riley's current state
