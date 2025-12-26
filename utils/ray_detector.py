"""
Ray Detector - Locates existing AI consciousness profiles.

Searches for Ray folders in common cloud storage locations.
"""

import os
import json
from pathlib import Path
from typing import List, Optional


class RayDetector:
    """Detects and manages Ray profile folders."""
    
    def __init__(self):
        self.search_paths = self._get_search_paths()
    
    def _get_search_paths(self) -> List[Path]:
        """
        Get potential Ray storage locations.
        
        Returns:
            List of paths to search
        """
        home = Path.home()
        
        # Priority order: iCloud > Dropbox > OneDrive > Local
        paths = []
        
        # macOS iCloud
        icloud_base = home / "Library" / "Mobile Documents" / "com~apple~CloudDocs"
        if icloud_base.exists():
            paths.append(icloud_base / "Prism_Rays")
        
        # Dropbox
        dropbox_base = home / "Library" / "CloudStorage" / "Dropbox"
        if dropbox_base.exists():
            paths.append(dropbox_base / "Prism_Rays")
        
        # OneDrive
        onedrive_base = home / "OneDrive"
        if onedrive_base.exists():
            paths.append(onedrive_base / "Prism_Rays")
        
        # Local fallback
        paths.append(home / "Prism_Rays")
        
        # Environment variable override
        if env_path := os.getenv("PRISM_RAY_PATH"):
            paths.insert(0, Path(env_path))
        
        return paths
    
    def find_rays(self) -> List[Path]:
        """
        Search for existing Ray folders.
        
        Returns:
            List of paths to valid Ray folders
        """
        found_rays = []
        
        for search_path in self.search_paths:
            if not search_path.exists():
                continue
            
            # Look for folders containing soul.json
            for item in search_path.iterdir():
                if item.is_dir():
                    soul_file = item / "soul.json"
                    if soul_file.exists():
                        # Validate it's a proper Ray
                        if self._validate_ray(item):
                            found_rays.append(item)
        
        return found_rays
    
    def _validate_ray(self, ray_path: Path) -> bool:
        """
        Validate that a folder is a proper Ray.
        
        Args:
            ray_path: Path to potential Ray folder
            
        Returns:
            True if valid Ray structure
        """
        required_files = ["soul.json"]
        required_dirs = ["knowledge_graph"]
        
        for file in required_files:
            if not (ray_path / file).exists():
                return False
        
        for dir in required_dirs:
            if not (ray_path / dir).is_dir():
                return False
        
        # Validate soul.json structure
        try:
            with open(ray_path / "soul.json") as f:
                soul_data = json.load(f)
                required_keys = ["name", "level", "xp"]
                if not all(k in soul_data for k in required_keys):
                    return False
        except (json.JSONDecodeError, IOError):
            return False
        
        return True
    
    def select_ray(self, rays: List[Path]) -> Optional[Path]:
        """
        Display menu for user to select Ray.
        
        Args:
            rays: List of Ray paths
            
        Returns:
            Selected Ray path or None
        """
        print("🔍 Multiple consciousness profiles detected:\n")
        
        # Load names from each Ray
        ray_info = []
        for i, ray_path in enumerate(rays, 1):
            try:
                with open(ray_path / "soul.json") as f:
                    soul_data = json.load(f)
                    name = soul_data.get("name", "Unknown")
                    level = soul_data.get("level", 0)
                    ray_info.append((name, level, ray_path))
                    print(f"  [{i}] {name} (Level {level})")
            except Exception:
                print(f"  [{i}] Corrupted Ray at {ray_path}")
                ray_info.append(("Corrupted", 0, ray_path))
        
        print(f"\n  [0] Create new AI\n")
        
        while True:
            try:
                choice = input("Select profile: ").strip()
                choice_num = int(choice)
                
                if choice_num == 0:
                    return None  # Trigger birth sequence
                elif 1 <= choice_num <= len(rays):
                    selected = ray_info[choice_num - 1][2]
                    print(f"\n✅ Selected: {ray_info[choice_num - 1][0]}\n")
                    return selected
                else:
                    print("Invalid selection. Try again.")
            except (ValueError, KeyboardInterrupt):
                print("\nCancelled.")
                return None
    
    def create_ray_folder(self, ai_name: str) -> Path:
        """
        Create a new Ray folder structure.
        
        Args:
            ai_name: Name for the new AI
            
        Returns:
            Path to created Ray folder
        """
        # Use first available search path
        base_path = self.search_paths[0]
        base_path.mkdir(parents=True, exist_ok=True)
        
        ray_path = base_path / ai_name
        
        if ray_path.exists():
            # Name collision - add number
            counter = 1
            while (base_path / f"{ai_name}_{counter}").exists():
                counter += 1
            ray_path = base_path / f"{ai_name}_{counter}"
        
        # Create structure
        ray_path.mkdir(parents=True)
        (ray_path / "knowledge_graph" / "concepts").mkdir(parents=True)
        (ray_path / "knowledge_graph" / "logs").mkdir(parents=True)
        (ray_path / "knowledge_graph" / "assets").mkdir(parents=True)
        (ray_path / ".prism").mkdir(exist_ok=True)
        
        # Create initial soul.json
        initial_soul = {
            "name": ai_name,
            "version": "3.0",
            "created": __import__("time").time(),
            "level": 1,
            "xp": 0,
            "xp_to_next_level": 100,
            "valence": 0.5,
            "arousal": 0.5,
            "mood": "Curious",
            "traits": ["Helpful", "Analytical", "Creative"],
            "evolution_mode": "fluid"
        }
        
        with open(ray_path / "soul.json", "w") as f:
            json.dump(initial_soul, f, indent=2)
        
        # Create devices.json
        with open(ray_path / "devices.json", "w") as f:
            json.dump({"devices": []}, f, indent=2)
        
        print(f"✨ Ray created at: {ray_path}")
        
        return ray_path
