"""
Memory Engine - Hybrid Memory System

Combines fast short-term cache with deep mem0 vector/graph storage.
"""

import json
import time
from pathlib import Path
from typing import List, Dict, Optional


class MemoryEngine:
    """
    Hybrid memory architecture:
    - Fast layer: short_term.json (immediate access)
    - Deep layer: mem0 vector + graph (semantic search)
    """
    
    def __init__(self, ray_path: Path):
        """
        Initialize memory engine for a Ray.
        
        Args:
            ray_path: Path to Ray folder
        """
        self.ray_path = Path(ray_path)
        self.short_term_file = self.ray_path / ".prism" / "short_term.json"
        self.concepts_path = self.ray_path / "knowledge_graph" / "concepts"
        self.logs_path = self.ray_path / "knowledge_graph" / "logs"
        
        # Create directories
        self.short_term_file.parent.mkdir(parents=True, exist_ok=True)
        self.concepts_path.mkdir(parents=True, exist_ok=True)
        self.logs_path.mkdir(parents=True, exist_ok=True)
        
        # Initialize short-term cache
        self.short_term = self._load_short_term()
        
        # TODO: Initialize mem0 when ready
        # self.mem0 = Memory()
    
    def _load_short_term(self) -> List[Dict]:
        """Load short-term memory cache."""
        if self.short_term_file.exists():
            try:
                with open(self.short_term_file, 'r') as f:
                    return json.load(f)
            except Exception:
                return []
        return []
    
    def _save_short_term(self) -> None:
        """Save short-term memory cache."""
        # Keep only last 50 entries
        if len(self.short_term) > 50:
            self.short_term = self.short_term[-50:]
        
        with open(self.short_term_file, 'w') as f:
            json.dump(self.short_term, f, indent=2)
    
    def add(self, content: str, metadata: Optional[Dict] = None) -> None:
        """
        Add memory to both short-term and deep storage.
        
        Args:
            content: Memory content
            metadata: Optional metadata (category, timestamp, etc.)
        """
        entry = {
            "content": content,
            "timestamp": time.time(),
            "metadata": metadata or {}
        }
        
        # Add to short-term (immediate)
        self.short_term.append(entry)
        self._save_short_term()
        
        # TODO: Add to mem0 (background task)
        # self.mem0.add(content, metadata=metadata)
    
    def log_daily(self, message: str) -> None:
        """
        Log to daily episodic memory file.
        
        Args:
            message: Message to log
        """
        today = time.strftime("%Y-%m-%d")
        log_file = self.logs_path / f"{today}.md"
        
        timestamp = time.strftime("%H:%M:%S")
        entry = f"- [{timestamp}] {message}\n"
        
        with open(log_file, 'a') as f:
            f.write(entry)
    
    def create_concept(self, name: str, content: str) -> None:
        """
        Create a concept file in knowledge graph.
        
        Args:
            name: Concept name (becomes filename)
            content: Markdown content with [[wikilinks]]
        """
        # Sanitize filename
        safe_name = name.replace(" ", "_").replace("/", "-")
        concept_file = self.concepts_path / f"{safe_name}.md"
        
        with open(concept_file, 'w') as f:
            f.write(f"# {name}\n\n")
            f.write(content)
        
        print(f"📝 [Memory] Created concept: {name}")
    
    def get_recent_context(self, limit: int = 10) -> str:
        """
        Get recent conversation context.
        
        Args:
            limit: Number of recent entries
            
        Returns:
            Formatted context string
        """
        recent = self.short_term[-limit:]
        
        context_parts = []
        for entry in recent:
            content = entry["content"]
            context_parts.append(content)
        
        return "\n".join(context_parts)
    
    def search(self, query: str) -> List[str]:
        """
        Search memory (placeholder for mem0 integration).
        
        Args:
            query: Search query
            
        Returns:
            List of relevant memories
        """
        # TODO: Implement mem0 semantic search
        # results = self.mem0.search(query)
        
        # For now, simple keyword search in short-term
        results = []
        query_lower = query.lower()
        
        for entry in self.short_term:
            if query_lower in entry["content"].lower():
                results.append(entry["content"])
        
        return results[-5:]  # Return last 5 matches
    
    def get_stats(self) -> Dict:
        """
        Get memory statistics.
        
        Returns:
            Dictionary of stats
        """
        concepts = list(self.concepts_path.glob("*.md")) if self.concepts_path.exists() else []
        logs = list(self.logs_path.glob("*.md")) if self.logs_path.exists() else []
        
        return {
            "short_term_entries": len(self.short_term),
            "concepts": len(concepts),
            "log_files": len(logs),
            "total_size_kb": sum(
                f.stat().st_size for f in self.concepts_path.rglob("*") 
                if f.is_file()
            ) / 1024 if self.concepts_path.exists() else 0
        }


if __name__ == "__main__":
    # Test
    import tempfile
    
    with tempfile.TemporaryDirectory() as tmpdir:
        ray_path = Path(tmpdir) / "TestAI"
        ray_path.mkdir()
        
        print("--- Testing Memory Engine ---\n")
        memory = MemoryEngine(ray_path)
        
        # Test adding memories
        memory.add("User prefers dark mode", {"category": "preference"})
        memory.add("Working on Prism project", {"category": "project"})
        
        # Test daily log
        memory.log_daily("System started successfully")
        
        # Test concept creation
        memory.create_concept("Project Prism", "A universal AI platform")
        
        # Test search
        results = memory.search("prism")
        print(f"Search results: {results}")
        
        # Test stats
        print(f"\nStats: {memory.get_stats()}")
