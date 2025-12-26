"""
Hybrid LLM System - Riley v2.0
Intelligently routes between Gemini (cloud/smart) and Ollama (local/private)
"""
import os
import google.generativeai as genai


class HybridLLM:
    """
    Multi-model LLM system that automatically routes requests
    to either Gemini (cloud) or Ollama (local) based on complexity.
    """
    
    def __init__(self):
        # Configure Gemini
        api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
            self.cloud = genai.GenerativeModel('gemini-1.5-flash')
            self.cloud_available = True
        else:
            self.cloud = None
            self.cloud_available = False
            print("⚠️ [Hybrid LLM] Gemini API key not set - cloud mode disabled")
        
        # Configure Ollama (local)
        try:
            from langchain_ollama import ChatOllama
            self.local = ChatOllama(model="llama3.2:1b", base_url="http://localhost:11434")
            self.local_available = True
        except ImportError:
            self.local = None
            self.local_available = False
            print("⚠️ [Hybrid LLM] langchain-ollama not installed - local mode disabled")
        
        print(f"🤖 [Hybrid LLM] Cloud: {self.cloud_available}, Local: {self.local_available}")
    
    def _classify_complexity(self, prompt):
        """
        Determines if a prompt is complex enough to warrant cloud processing.
        
        Returns: 'smart' or 'simple'
        """
        # Keywords that indicate complex tasks
        complex_keywords = [
            "analyze", "explain", "complex", "detailed", "research",
            "comprehensive", "elaborate", "philosophy", "nuanced"
        ]
        
        simple_keywords = [
            "what is", "define", "list", "short", "brief", "quick"
        ]
        
        prompt_lower = prompt.lower()
        
        # Check for complexity indicators
        has_complex = any(keyword in prompt_lower for keyword in complex_keywords)
        has_simple = any(keyword in prompt_lower for keyword in simple_keywords)
        
        # Length-based heuristic
        if len(prompt) > 200:
            return "smart"
        
        if has_complex and not has_simple:
            return "smart"
        
        return "simple"
    
    def generate(self, prompt, mode="auto", max_tokens=1000):
        """
        Generates a response using the appropriate model.
        
        Args:
            prompt: str - The prompt to send
            mode: str - "auto", "smart" (Gemini), or "simple" (Ollama)
            max_tokens: int - Maximum response length
        
        Returns:
            str - Generated response
        """
        # Determine routing
        if mode == "auto":
            complexity = self._classify_complexity(prompt)
        else:
            complexity = mode
        
        # Route to appropriate model
        try:
            if complexity == "smart" and self.cloud_available:
                print("☁️ [Hybrid] Using Gemini (cloud)")
                response = self.cloud.generate_content(prompt)
                return response.text
            
            elif self.local_available:
                print("💻 [Hybrid] Using Ollama (local)")
                response = self.local.invoke(prompt)
                return response.content
            
            elif self.cloud_available:
                # Fallback to cloud if local not available
                print("☁️ [Hybrid] Fallback to Gemini")
                response = self.cloud.generate_content(prompt)
                return response.text
            
            else:
                return "Error: No LLM available (neither Gemini nor Ollama configured)"
                
        except Exception as e:
            print(f"⚠️ [Hybrid] Generation error: {e}")
            return f"Error: {str(e)[:100]}"


if __name__ == "__main__":
    # Test Hybrid LLM
    print("🧪 Testing Hybrid LLM\n")
    
    llm = HybridLLM()
    
    # Test 1: Simple prompt (should use local)
    print("\n--- Test 1: Simple Prompt ---")
    response1 = llm.generate("What is 2+2?")
    print(f"Response: {response1}\n")
    
    # Test 2: Complex prompt (should use cloud)
    print("\n--- Test 2: Complex Prompt ---")
    response2 = llm.generate("Provide a detailed philosophical analysis of consciousness")
    print(f"Response: {response2[:200]}...\n")
    
    # Test 3: Force mode selection
    print("\n--- Test 3: Force Smart Mode ---")
    response3 = llm.generate("Hello", mode="smart")
    print(f"Response: {response3}")
