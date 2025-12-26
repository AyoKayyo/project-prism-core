import os
from mem0 import Memory
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

# CONFIG: Force Mem0 to use Google Gemini for everything
# This prevents it from asking for an OpenAI key
config = {
    "llm": {
        "provider": "gemini",
        "config": {
            "model": "gemini-2.0-flash-lite",
            "temperature": 0.1,
            "max_tokens": 1500,
        }
    },
    "embedder": {
        "provider": "gemini",
        "config": {
            "model": "models/text-embedding-004"
        }
    },
    "vector_store": {
        "provider": "chroma",
        "config": {
            "collection_name": "riley_memory",
            "path": "db",
        }
    }
}

class RileyMemory:
    def __init__(self):
        # Initialize Mem0 with Gemini Config
        # It will use the GEMINI_API_KEY from your .env automatically
        # (Ensure your .env has GEMINI_API_KEY=AIza...)
        os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")
        self.memory = Memory.from_config(config)
        self.user_id = "mark_k"

    def add_interaction(self, user_text, ai_text):
        """Stores a conversation pair into long-term memory"""
        messages = [
            {"role": "user", "content": user_text},
            {"role": "assistant", "content": ai_text}
        ]
        self.memory.add(messages, user_id=self.user_id)
        print(f"🧠 [Memory] Stored: {user_text[:30]}...")

    def log_episode(self, source, event):
        """Stores a timestamped event into episodic memory (The Journal)"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"[{timestamp}] [{source}] {event}"
        
        # We store this as a 'user' message to the brain so it remembers what happened
        # Ideally, we'd separate this, but for Mem0 v1, we treat it as an observation.
        messages = [
            {"role": "user", "content": f"I just observed/did this: {entry}"},
            {"role": "assistant", "content": "Logged."}
        ]
        self.memory.add(messages, user_id=self.user_id)
        print(f"📓 [Journal] {entry}")

    def recall(self, query):
        """Searches for relevant past facts"""
        print(f"🔍 [Thinking] Searching memory for: '{query}'...")
        results = self.memory.search(query, user_id=self.user_id)
        
        if not results:
            return ""
        
        # Extract the text from the search results
        facts = []
        for res in results:
             if isinstance(res, dict):
                 facts.append(res.get('memory', str(res)))
             else:
                 facts.append(str(res))
                 
        return "\n".join(facts)

# --- TEST LAB ---
if __name__ == "__main__":
    brain = RileyMemory()
    
    # Test 1: Log an Episode
    print("--- Journaling Phase ---")
    brain.log_episode("SYSTEM", "User opened VS Code")
    brain.log_episode("SENSES", "Battery dropped to 40%")
    
    # Test 2: Recall
    print("\n--- Recall Phase ---")
    fact = brain.recall("What happened with the battery?")
    print(f"✅ RILEY REMEMBERS:\n{fact}")
