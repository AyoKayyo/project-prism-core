"""
Obsidian Brain Core - Riley v2.0
Markdown-based knowledge graph with Wikilinks for semantic memory
"""
import os
import time
from pathlib import Path
from datetime import datetime
import re
from soul_structure import SoulCartridge


class ObsidianBrain:
    """
    Knowledge management system using Obsidian-style Markdown with Wikilinks.
    Each concept is a .md file with [[WikiLinks]] to related concepts.
    """
    
    def __init__(self):
        # Initialize Soul Cartridge
        self.cartridge = SoulCartridge()
        self.cartridge.init_soul_cartridge()
        
        self.vault_path = self.cartridge.soul_path / "knowledge_graph"
        self.concepts_path = self.cartridge.concepts_path
        self.logs_path = self.cartridge.logs_path
        self.assets_path = self.cartridge.assets_path
        
        print(f"🧠 [Brain] Obsidian Vault at: {self.vault_path}")
    
    def learn(self, concept_name, content, related_links=None):
        """
        Creates or updates a concept node in the knowledge graph.
        
        Args:
            concept_name: Name of the concept (becomes filename)
            content: Markdown content
            related_links: List of related concept names for [[Wikilinks]]
        """
        # Sanitize filename
        safe_name = re.sub(r'[<>:"/\\|?*]', '_', concept_name)
        concept_file = self.concepts_path / f"{safe_name}.md"
        
        # Build content with metadata
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        frontmatter = f"""---
created: {timestamp}
tags: [concept]
---

"""
        
        # Add wikilinks if provided
        if related_links:
            links_section = "\n## Related Concepts\n" + "\n".join([f"- [[{link}]]" for link in related_links])
            full_content = frontmatter + content + "\n" + links_section
        else:
            full_content = frontmatter + content
        
        # Write file
        with open(concept_file, 'w', encoding='utf-8') as f:
            f.write(full_content)
        
        print(f"📝 [Brain] Learned: {concept_name}")
        return str(concept_file)
    
    def recall(self, query):
        """
        Searches concepts by keyword (simple grep-style search).
        Returns list of matching concept names.
        """
        matches = []
        query_lower = query.lower()
        
        for concept_file in self.concepts_path.glob("*.md"):
            # Search in filename
            if query_lower in concept_file.stem.lower():
                matches.append(concept_file.stem)
                continue
            
            # Search in content
            try:
                with open(concept_file, 'r', encoding='utf-8') as f:
                    content = f.read().lower()
                    if query_lower in content:
                        matches.append(concept_file.stem)
            except Exception as e:
                print(f"⚠️ Error reading {concept_file}: {e}")
        
        return matches
    
    def log_daily(self, entry):
        """
        Appends to today's daily log in logs/ directory.
        """
        today = datetime.now().strftime("%Y-%m-%d")
        log_file = self.logs_path / f"{today}.md"
        
        # Create file with header if it doesn't exist
        if not log_file.exists():
            with open(log_file, 'w', encoding='utf-8') as f:
                f.write(f"# Daily Log: {today}\n\n")
        
        # Append entry with timestamp
        timestamp = datetime.now().strftime("%H:%M:%S")
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(f"**{timestamp}** - {entry}\n\n")
        
        return str(log_file)
    
    def save_visual_memory(self, image_data, description):
        """
        Saves image to assets/ and links it in a memory node.
        
        Args:
            image_data: bytes of the image
            description: text description from visual analysis
        """
        timestamp = int(time.time())
        filename = f"vision_{timestamp}.png"
        asset_path = self.assets_path / filename
        
        # Save Image Bytes
        with open(asset_path, "wb") as f:
            f.write(image_data)
        
        # Create Memory Node
        content = f"![[{filename}]]\n\n**Visual Analysis:** {description}"
        concept_name = f"Visual_Memory_{timestamp}"
        self.learn(concept_name, content, related_links=["Visual Cortex"])
        
        print(f"👁️ [Brain] Saved visual memory: {filename}")
        return concept_name
    
    def update_core_fact(self, category, fact):
        """
        Updates specific sections in Core_Knowledge.md
        
        Args:
            category: Section name (e.g., "User Preferences")
            fact: The fact to append
        """
        core_file = self.concepts_path / "Core_Knowledge.md"
        timestamp = datetime.now().strftime("%Y-%m-%d")
        entry = f"\n- [{timestamp}] **{category}:** {fact}"
        
        # Read existing content
        if core_file.exists():
            with open(core_file, 'r', encoding='utf-8') as f:
                content = f.read()
        else:
            content = "# Core Knowledge\n\n## User Preferences\n\n## System Facts\n\n"
        
        # Simple append for now (in production, use regex to find section)
        with open(core_file, "a", encoding="utf-8") as f:
            f.write(entry)
        
        print(f"💾 [Brain] Updated Core Knowledge: {category}")
        return str(core_file)
    
    def define_relationship(self, entity_a, relation, entity_b):
        """
        Creates an explicit relationship edge in the knowledge graph.
        Format: [[Entity A]] -- relation --> [[Entity B]]
        """
        rel_file = self.vault_path / "Relationship_Graph.md"
        entry = f"- [[{entity_a}]] -- *{relation}* --> [[{entity_b}]]\n"
        
        with open(rel_file, "a", encoding="utf-8") as f:
            f.write(entry)
        
        print(f"🔗 [Graph] New Edge: {entity_a} -> {entity_b}")
        return entry
    
    def get_concept(self, concept_name):
        """
        Retrieves the full content of a concept by name.
        """
        safe_name = re.sub(r'[<>:"/\\|?*]', '_', concept_name)
        concept_file = self.concepts_path / f"{safe_name}.md"
        
        if concept_file.exists():
            with open(concept_file, 'r', encoding='utf-8') as f:
                return f.read()
        return None
    
    def get_today_log(self):
        """Returns today's log content"""
        today = datetime.now().strftime("%Y-%m-%d")
        log_file = self.logs_path / f"{today}.md"
        
        if log_file.exists():
            with open(log_file, 'r', encoding='utf-8') as f:
                return f.read()
        return None


# Backward compatibility - maintain old name
RileyMemory = ObsidianBrain


if __name__ == "__main__":
    # Test Obsidian Brain
    print("🧪 Testing Obsidian Brain Core\n")
    
    brain = ObsidianBrain()
    
    # Test 1: Learn a concept
    brain.learn("Python", "A high-level programming language", ["Technology", "Programming"])
    
    # Test 2: Log daily entry
    brain.log_daily("Started testing Obsidian Brain Core")
    
    # Test 3: Define relationship
    brain.define_relationship("Riley", "loves", "Python")
    
    # Test 4: Recall
    matches = brain.recall("python")
    print(f"\n🔍 Recall 'python': {matches}")
    
    # Test 5: Update core fact
    brain.update_core_fact("User Preferences", "Prefers dark mode")
    
    print("\n✅ Obsidian Brain tests complete!")
