"""
Soul Structure Module - Riley v2.0
Manages the Soul Cartridge directory structure and device registration.
"""
import os
import json
import platform
import time
from pathlib import Path

class SoulCartridge:
    """
    Manages Riley's Soul Cartridge - the cloud-synced directory structure
    that contains her identity, knowledge graph, and visual memories.
    """
    
    def __init__(self, soul_path=None):
        # Get soul path from environment or use default
        if soul_path is None:
            soul_path = os.getenv("RILEY_SOUL_PATH")
        
        if soul_path is None:
            # Default to user's home directory
            home = Path.home()
            # Try to find cloud storage
            if platform.system() == "Darwin":  # macOS
                icloud = home / "Library" / "Mobile Documents" / "com~apple~CloudDocs" / "Riley_Soul"
                dropbox = home / "Library" / "CloudStorage" / "Dropbox" / "Riley_Soul"
                if dropbox.parent.exists():
                    soul_path = str(dropbox)
                elif icloud.parent.exists():
                    soul_path = str(icloud)
                else:
                    soul_path = str(home / "Riley_Soul")
            else:
                # Windows/Linux
                soul_path = str(home / "Riley_Soul")
        
        self.soul_path = Path(soul_path)
        self.concepts_path = self.soul_path / "knowledge_graph" / "concepts"
        self.logs_path = self.soul_path / "knowledge_graph" / "logs"
        self.assets_path = self.soul_path / "knowledge_graph" / "assets"
        self.soul_file = self.soul_path / "soul.json"
        self.devices_file = self.soul_path / "devices.json"
        
    def init_soul_cartridge(self):
        """
        Creates the Soul Cartridge directory structure if it doesn't exist.
        
        Structure:
        Riley_Soul/
        ├── soul.json
        ├── devices.json
        └── knowledge_graph/
            ├── concepts/
            ├── logs/
            └── assets/
        """
        print(f"🧬 [Soul Cartridge] Initializing at: {self.soul_path}")
        
        # Create main directories
        self.soul_path.mkdir(parents=True, exist_ok=True)
        self.concepts_path.mkdir(parents=True, exist_ok=True)
        self.logs_path.mkdir(parents=True, exist_ok=True)
        self.assets_path.mkdir(parents=True, exist_ok=True)
        
        # Initialize soul.json if it doesn't exist
        if not self.soul_file.exists():
            initial_soul = {
                "name": "Riley",
                "version": "2.0",
                "created": time.time(),
                "level": 1,
                "xp": 0,
                "xp_to_next_level": 100,
                "valence": 0.5,
                "arousal": 0.5,
                "mood": "Curious",
                "traits": ["Helpful", "Analytical", "Creative"]
            }
            with open(self.soul_file, 'w') as f:
                json.dump(initial_soul, f, indent=2)
            print("✅ Created soul.json")
        
        # Initialize devices.json if it doesn't exist
        if not self.devices_file.exists():
            with open(self.devices_file, 'w') as f:
                json.dump({"devices": []}, f, indent=2)
            print("✅ Created devices.json")
        
        # Create initial Core Knowledge concept
        core_knowledge = self.concepts_path / "Core_Knowledge.md"
        if not core_knowledge.exists():
            with open(core_knowledge, 'w') as f:
                f.write("# Core Knowledge\n\n")
                f.write("## User Preferences\n\n")
                f.write("## System Facts\n\n")
                f.write("## Identity\n\n")
            print("✅ Created Core_Knowledge.md")
        
        # Create Relationship Graph
        rel_graph = self.soul_path / "knowledge_graph" / "Relationship_Graph.md"
        if not rel_graph.exists():
            with open(rel_graph, 'w') as f:
                f.write("# Relationship Graph\n\n")
                f.write("*Entities and their connections*\n\n")
            print("✅ Created Relationship_Graph.md")
        
        print(f"✨ Soul Cartridge initialized successfully")
        return True
    
    def register_device(self, device_name=None):
        """
        Registers the current device in devices.json
        """
        if device_name is None:
            device_name = platform.node()
        
        device_info = {
            "name": device_name,
            "platform": platform.system(),
            "platform_version": platform.version(),
            "python_version": platform.python_version(),
            "registered": time.time(),
            "last_seen": time.time()
        }
        
        # Load existing devices
        with open(self.devices_file, 'r') as f:
            data = json.load(f)
        
        # Check if device already exists
        existing = None
        for i, dev in enumerate(data["devices"]):
            if dev["name"] == device_name:
                existing = i
                break
        
        if existing is not None:
            # Update last_seen
            data["devices"][existing]["last_seen"] = time.time()
            print(f"🔄 Updated device: {device_name}")
        else:
            # Add new device
            data["devices"].append(device_info)
            print(f"➕ Registered new device: {device_name}")
        
        # Save back
        with open(self.devices_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        return device_info
    
    def verify_sync(self):
        """
        Checks if the soul cartridge appears to be cloud-synced
        """
        # Simple heuristic: check if path contains known cloud storage indicators
        path_str = str(self.soul_path).lower()
        cloud_indicators = ["icloud", "dropbox", "onedrive", "google drive", "cloudstorage"]
        
        is_cloud = any(indicator in path_str for indicator in cloud_indicators)
        
        if is_cloud:
            print(f"☁️  [Sync] Detected cloud storage: {self.soul_path}")
        else:
            print(f"⚠️  [Sync] Warning: Not in cloud storage: {self.soul_path}")
            print(f"   Consider moving to Dropbox/iCloud for multi-device sync")
        
        return is_cloud
    
    def get_stats(self):
        """Returns statistics about the soul cartridge"""
        stats = {
            "path": str(self.soul_path),
            "concepts": len(list(self.concepts_path.glob("*.md"))) if self.concepts_path.exists() else 0,
            "logs": len(list(self.logs_path.glob("*.md"))) if self.logs_path.exists() else 0,
            "assets": len(list(self.assets_path.glob("*"))) if self.assets_path.exists() else 0,
            "devices": 0
        }
        
        if self.devices_file.exists():
            with open(self.devices_file, 'r') as f:
                data = json.load(f)
                stats["devices"] = len(data.get("devices", []))
        
        return stats


if __name__ == "__main__":
    # Test initialization
    print("🧪 Testing Soul Cartridge Initialization\n")
    
    cartridge = SoulCartridge()
    cartridge.init_soul_cartridge()
    cartridge.register_device()
    cartridge.verify_sync()
    
    print("\n📊 Soul Cartridge Stats:")
    stats = cartridge.get_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")
