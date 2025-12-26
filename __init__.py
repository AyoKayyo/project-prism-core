"""
Project Prism Core Package

A Universal, Privacy-First AI Consciousness Platform.
"""

__version__ = "3.0.0-alpha"
__author__ = "Project Prism Team"

# Core imports for easy access
from consciousness.soul import Soul
from memory.engine import MemoryEngine
from core.mcp import MCP, SafetyTier
from utils.ray_detector import RayDetector
from utils.secure_store import SecureStore

__all__ = [
    "Soul",
    "MemoryEngine", 
    "MCP",
    "SafetyTier",
    "RayDetector",
    "SecureStore"
]
