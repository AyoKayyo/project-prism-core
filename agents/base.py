"""
Base Agent - Abstract class for all specialized agents.
"""

from abc import ABC, abstractmethod
from typing import Optional, Dict
from utils.secure_store import SecureStore


class BaseAgent(ABC):
    """
    Base class for all AI agents.
    
    Provides common functionality:
    - Model configuration
    - API key access (via SecureStore)
    - Safety integration
    """
    
    def __init__(self, model_name: str, agent_name: str):
        """
        Initialize base agent.
        
        Args:
            model_name: LLM model identifier
            agent_name: Human-readable agent name
        """
        self.model_name = model_name
        self.agent_name = agent_name
        self.system_prompt = ""
    
    def get_api_key(self, key_name: str = "GEMINI_API_KEY") -> Optional[str]:
        """
        Retrieve API key from SecureStore (Ghost Protocol).
        
        Args:
            key_name: Key identifier
            
        Returns:
            API key or None
        """
        return SecureStore.get(key_name)
    
    @abstractmethod
    def execute(self, user_input: str, context: Optional[Dict] = None) -> str:
        """
        Execute agent's primary function.
        
        Args:
            user_input: User's request
            context: Optional context dictionary
            
        Returns:
            Agent's response
        """
        pass
    
    def set_system_prompt(self, prompt: str) -> None:
        """
        Set agent's system prompt.
        
        Args:
            prompt: System prompt text
        """
        self.system_prompt = prompt
    
    def estimate_tokens(self, text: str) -> int:
        """
        Estimate token count for text.
        
        Args:
            text: Text to estimate
            
        Returns:
            Estimated token count
        """
        # Rough estimation: ~4 chars per token
        return len(text) // 4
