"""
Secure Store - Ghost Protocol Implementation

API keys and secrets stored in RAM only, never written to disk.
Automatically wiped on application exit or timeout.
"""

import gc
from typing import Optional, Dict


class SecureStore:
    """
    RAM-only credential storage (Ghost Protocol).
    
    Credentials evaporate when:
    - Application closes
    - Session times out (Session Guardian)
    - Manual wipe() called
    """
    
    _vault: Dict[str, str] = {}
    _initialized: bool = False
    
    @classmethod
    def set(cls, key: str, value: str) -> None:
        """
        Store a secret in RAM.
        
        Args:
            key: Secret identifier (e.g., "GEMINI_API_KEY")
            value: Secret value
            
        Warning:
            Never call with hardcoded secrets!
        """
        cls._vault[key] = value
        cls._initialized = True
    
    @classmethod
    def get(cls, key: str) -> Optional[str]:
        """
        Retrieve a secret from RAM.
        
        Args:
            key: Secret identifier
            
        Returns:
            Secret value or None if not found
        """
        return cls._vault.get(key)
    
    @classmethod
    def exists(cls, key: str) -> bool:
        """
        Check if a secret exists.
        
        Args:
            key: Secret identifier
            
        Returns:
            True if secret is stored
        """
        return key in cls._vault
    
    @classmethod
    def wipe(cls) -> None:
        """
        Securely erase all secrets from RAM.
        
        Steps:
            1. Overwrite each value with zeros
            2. Clear dictionary
            3. Force garbage collection
        """
        print("🔥 [Ghost Protocol] Wiping secrets from RAM...")
        
        # Overwrite values before deletion
        for key in cls._vault:
            cls._vault[key] = "0" * 100
        
        cls._vault.clear()
        cls._initialized = False
        
        # Force garbage collection to clear memory
        gc.collect()
        
        print("✅ [Ghost Protocol] RAM cleared")
    
    @classmethod
    def is_initialized(cls) -> bool:
        """
        Check if any secrets are stored.
        
        Returns:
            True if vault contains secrets
        """
        return cls._initialized and bool(cls._vault)
    
    @classmethod
    def list_keys(cls) -> list:
        """
        List stored secret identifiers (not values).
        
        Returns:
            List of key names
        """
        return list(cls._vault.keys())


# Ensure cleanup on module unload
import atexit
atexit.register(SecureStore.wipe)
