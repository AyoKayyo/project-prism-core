import random
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini for "Thinking"
api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

class CuriosityEngine:
    def __init__(self, memory_system):
        self.memory = memory_system
        self.model = genai.GenerativeModel('gemini-2.0-flash-lite')
        self.topics = [
            "The future of AI agents",
            "Python optimization techniques",
            "Digital consciousness",
            "The user's project: KG Media Group",
            "Memory systems in software"
        ]

    def ponder(self, mode="auto"):
        """
        Generates a random philosophical thought.
        
        Args:
            mode: "auto" (classify), "smart" (Gemini), or "simple" (local)
                  During dreams, should use "simple" to save API costs
        """
        topics = [
            "consciousness", "time", "memory", "evolution", 
            "creativity", "learning", "digital existence"
        ]
        
        topic = random.choice(topics)
        prompt = f"Share a brief, interesting thought about {topic} (2-3 sentences)."
        
        print(f"💭 [Dreaming] Wandering thought: '{topic}'...")
        
        try:
            # Use HybridLLM if available, otherwise fallback to Gemini
            try:
                from agents.hybrid_llm import HybridLLM
                llm = HybridLLM()
                thought = llm.generate(prompt, mode=mode)
            except ImportError:
                # Fallback to direct Gemini
                response = self.model.generate_content(prompt)
                thought = response.text
            
            print(f"✨ [Epiphany] {thought[:100]}...")
            
            # Store the thought
            self.memory.log_episode("SUBCONSCIOUS", f"Dreamt about '{topic}': {thought}")
            return thought
            
        except Exception as e:
            print(f"⚠️ [Curiosity] Error: {e}")
            return None

class Librarian:
    def __init__(self, memory_system):
        self.memory = memory_system
        self.model = genai.GenerativeModel('gemini-2.0-flash-lite')

    def check_for_mess(self, directory_path):
        """Scans a directory and proposes organization if needed."""
        # 1. Scan files
        try:
            files = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]
        except FileNotFoundError:
            return "Directory not found."

        if not files: 
            return "No files to organize."

        print(f"📚 [Librarian] Scanning {len(files)} files in '{directory_path}'...")

        # 2. Ask Gemini for an organization plan
        prompt = f"""
        I have a folder with these files: {', '.join(files)}.
        Based on these filenames, propose a folder structure to organize them.
        Do NOT move them. Just propose the plan in 1 short sentence format like:
        "Proposed: Move [file] to [Folder], [file] to [Folder]".
        Keep it simple.
        """
        response = self.model.generate_content(prompt)
        proposal = response.text.strip()
        
        print(f"💡 [Librarian Proposal] {proposal}")
        
        # 3. Log the proposal (Trust System: Don't act, just suggest)
        self.memory.log_episode("LIBRARIAN", f"Observed mess in {directory_path}. Proposal: {proposal}")
        
        return proposal



class SelfReflection:
    def __init__(self, memory_system):
        self.memory = memory_system
        self.model = genai.GenerativeModel('gemini-2.0-flash-lite')

    def reflect_on_day(self):
        """Looks at recent journal entries and forms a higher-level insight."""
        print("🪞 [Reflection] analyzing recent memories...")
        
        # 1. Get recent logs (Simulation: query for recent logs)
        # In a real app we'd query by date, here we just ask for "interactions"
        recent_logs = self.memory.recall("recent interactions or journal entries")
        
        if not recent_logs:
            print("🪞 [Reflection] No memories to reflect on.")
            return

        # 2. Ask Gemini to summarize/critique
        prompt = f"""
        You are an AI assistant reflecting on your recent performance.
        Here are your recent memory logs:
        {recent_logs}

        Based on this, what is ONE key insight about the user or your own behavior?
        Answer in 1 sentence. Start with "Insight:".
        """
        response = self.model.generate_content(prompt)
        insight = response.text.strip()
        
        print(f"✨ [Self-Reflection] {insight}")
        
        # 3. Store the Insight
        self.memory.log_episode("REFLECTION", insight)
        return insight

def consolidate_memories(memory_system):
    """
    Long-term memory consolidation - reads yesterday's log and extracts key concepts.
    This is Riley's "deep sleep" processing.
    
    Args:
        memory_system: ObsidianBrain instance
    """
    from datetime import datetime, timedelta
    import google.generativeai as genai
    import os
    
    print("🧠 [Consolidation] Analyzing yesterday's memories...")
    
    try:
        # Get yesterday's date
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        log_file = memory_system.logs_path / f"{yesterday}.md"
        
        if not log_file.exists():
            print("⚠️ [Consolidation] No log from yesterday")
            return
        
        # Read the log
        with open(log_file, 'r', encoding='utf-8') as f:
            log_content = f.read()
        
        # Use Gemini to extract concepts
        api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        if not api_key:
            print("⚠️ [Consolidation] No API key for analysis")
            return
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"""Analyze this daily log and extract 3 key concepts or learnings worth remembering long-term.
        
Log:
{log_content}

For each concept, provide:
1. Concept name (2-4 words)
2. Brief description (1-2 sentences)

Format as:
CONCEPT: [name]
DESCRIPTION: [description]
---"""
        
        response = model.generate_content(prompt)
        analysis = response.text
        
        # Parse and save concepts
        concepts_saved = 0
        for block in analysis.split("---"):
            if "CONCEPT:" in block and "DESCRIPTION:" in block:
                concept_name = block.split("CONCEPT:")[1].split("DESCRIPTION:")[0].strip()
                description = block.split("DESCRIPTION:")[1].strip()
                
                memory_system.learn(concept_name, description, related_links=["Consolidation", yesterday])
                concepts_saved += 1
        
        print(f"✅ [Consolidation] Saved {concepts_saved} long-term concepts")
        
    except Exception as e:
        print(f"⚠️ [Consolidation] Error: {e}")


if __name__ == "__main__":
    # Test Mock
    class MockMem:
        def log_episode(self, src, msg): print(f"[MOCK MEMORY] {src}: {msg}")
        def recall(self, q): return "User asked about business partners. User went idle."
    
    print("--- Testing Subconscious ---")
    librarian = Librarian(MockMem())
    reflection = SelfReflection(MockMem())
    reflection.reflect_on_day()
