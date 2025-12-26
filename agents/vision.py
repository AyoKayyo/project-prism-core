"""
Visual Cortex - Riley v2.0
Screenshot capture and analysis using Gemini Vision API
"""
import os
import io
from PIL import Image
import pyautogui
import google.generativeai as genai
from pathlib import Path


class VisionAgent:
    """
    Riley's Visual Cortex - capable of capturing and analyzing screenshots.
    Stores visual memories in the Obsidian Brain.
    """
    
    def __init__(self, memory_system):
        self.memory = memory_system
        
        # Configure Gemini Vision
        api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY or GOOGLE_API_KEY not set")
        
        genai.configure(api_key=api_key)
        self.vision_model = genai.GenerativeModel('gemini-1.5-flash')
        
        print("👁️ [Vision] Visual Cortex initialized")
    
    def capture_screen(self):
        """
        Captures the current screen as a PIL Image.
        Returns: PIL.Image object
        """
        try:
            screenshot = pyautogui.screenshot()
            print("📸 [Vision] Screenshot captured")
            return screenshot
        except Exception as e:
            print(f"⚠️ [Vision] Screenshot failed: {e}")
            return None
    
    def analyze_visual(self, image):
        """
        Sends image to Gemini Vision for analysis.
        
        Args:
            image: PIL.Image object
        
        Returns:
            str: Analysis description
        """
        try:
            # Prepare prompt
            prompt = """Analyze this screenshot and describe:
1. What application or activity is shown
2. Key visual elements (UI, content, etc.)
3. What the user might be doing
4. Any notable text or information visible

Keep the description concise (2-3 sentences)."""
            
            # Generate analysis
            response = self.vision_model.generate_content([prompt, image])
            analysis = response.text
            
            print(f"🧠 [Vision] Analysis complete")
            return analysis
            
        except Exception as e:
            print(f"⚠️ [Vision] Analysis failed: {e}")
            return f"Analysis error: {str(e)[:100]}"
    
    def save_to_vault(self, image, analysis):
        """
        Saves screenshot and analysis to Obsidian Vault.
        
        Args:
            image: PIL.Image object
            analysis: str description
        
        Returns:
            str: Concept name created
        """
        # Convert image to bytes
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        image_bytes = img_byte_arr.getvalue()
        
        # Save to memory system
        concept_name = self.memory.save_visual_memory(image_bytes, analysis)
        
        return concept_name
    
    def observe(self):
        """
        Full observation cycle: capture, analyze, save.
        Returns: tuple (success, concept_name)
        """
        # Capture
        image = self.capture_screen()
        if image is None:
            return False, None
        
        # Analyze
        analysis = self.analyze_visual(image)
        
        # Save
        concept_name = self.save_to_vault(image, analysis)
        
        print(f"✅ [Vision] Observation complete: {concept_name}")
        return True, concept_name


if __name__ == "__main__":
    # Test Visual Cortex
    print("🧪 Testing Visual Cortex\n")
    
    from lab_memory import ObsidianBrain
    
    brain = ObsidianBrain()
    vision = VisionAgent(brain)
    
    print("\n📸 Capturing and analyzing current screen...")
    success, concept = vision.observe()
    
    if success:
        print(f"\n✅ Visual memory saved: {concept}")
        print("Check your Soul Cartridge assets/ folder for the screenshot")
    else:
        print("\n❌ Visual observation failed")
