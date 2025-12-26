"""
Specialized Cloud Agents Configuration

Maps agent types to their optimal cloud services and defines
how natural language gets translated to service-specific prompts.
"""

from typing import Dict, List
from enum import Enum


class CloudService(Enum):
    """Available cloud AI services."""
    GEMINI = "gemini"
    GPT = "gpt"
    CLAUDE = "claude"
    PERPLEXITY = "perplexity"
    LOCAL = "local"


class AgentType(Enum):
    """Specialized agent roles."""
    RESEARCHER = "researcher"
    CODER = "coder"
    ARCHITECT = "architect"
    ANALYST = "analyst"
    WRITER = "writer"
    VISION = "vision"
    COMPANION = "companion"


# Agent → Cloud Service Routing
AGENT_SERVICE_MAP: Dict[AgentType, CloudService] = {
    AgentType.RESEARCHER: CloudService.PERPLEXITY,  # Deep web research
    AgentType.CODER: CloudService.CLAUDE,           # Code generation
    AgentType.ARCHITECT: CloudService.GEMINI,       # System design
    AgentType.ANALYST: CloudService.GPT,            # Data analysis
    AgentType.WRITER: CloudService.CLAUDE,          # Long-form content
    AgentType.VISION: CloudService.GEMINI,          # Image analysis
    AgentType.COMPANION: CloudService.LOCAL,        # Privacy-first chat
}


# Service-specific API configurations
SERVICE_CONFIG = {
    CloudService.GEMINI: {
        "model": "gemini-2.0-flash-exp",
        "api_base": "https://generativelanguage.googleapis.com/v1beta",
        "env_key": "GEMINI_API_KEY",
        "max_tokens": 8192,
        "temperature": 0.7,
    },
    CloudService.GPT: {
        "model": "gpt-4-turbo-preview",
        "api_base": "https://api.openai.com/v1",
        "env_key": "OPENAI_API_KEY",
        "max_tokens": 4096,
        "temperature": 0.7,
    },
    CloudService.CLAUDE: {
        "model": "claude-3-5-sonnet-20241022",
        "api_base": "https://api.anthropic.com/v1",
        "env_key": "ANTHROPIC_API_KEY",
        "max_tokens": 8192,
        "temperature": 0.7,
    },
    CloudService.PERPLEXITY: {
        "model": "llama-3.1-sonar-huge-128k-online",
        "api_base": "https://api.perplexity.ai",
        "env_key": "PERPLEXITY_API_KEY",
        "max_tokens": 4096,
        "temperature": 0.2,  # Lower for factual research
    },
    CloudService.LOCAL: {
        "model": "llama3.1:8b",
        "api_base": "http://localhost:11434",
        "env_key": None,  # No API key for local
        "max_tokens": 2048,
        "temperature": 0.8,
    },
}


# Agent-specific system prompts
AGENT_SYSTEM_PROMPTS = {
    AgentType.RESEARCHER: """You are a deep research specialist with real-time web access.
Your role: Conduct comprehensive research using current sources.
Output format: Structured findings with citations.
Always include source URLs and publish dates.
Prioritize recent, authoritative sources.""",
    
    AgentType.CODER: """You are an expert software engineer using Claude's advanced reasoning.
Your role: Write production-quality, well-documented code.
Output format: Complete, functional code with explanations.
Best practices: Follow language conventions, add error handling, include tests.
Always explain architectural decisions.""",
    
    AgentType.ARCHITECT: """You are a system design architect with Gemini's multimodal capabilities.
Your role: Design scalable, maintainable system architectures.
Output format: Technical specifications with diagrams (if needed).
Consider: Performance, security, cost, maintainability.
Provide trade-off analysis.""",
    
    AgentType.ANALYST: """You are a data analyst using GPT's reasoning capabilities.
Your role: Analyze data, identify patterns, provide insights.
Output format: Clear findings with statistical backing.
Include: Visualizations (describe), confidence levels, recommendations.""",
    
    AgentType.WRITER: """You are a professional writer using Claude's long-form capabilities.
Your role: Create engaging, well-structured content.
Output format: Polished prose appropriate to context.
Adapt tone: From technical documentation to creative narratives.""",
    
    AgentType.VISION: """You are a vision specialist using Gemini's multimodal AI.
Your role: Analyze images, screenshots, diagrams.
Output format: Detailed descriptions with insights.
Extract: Text, objects, layouts, patterns, anomalies.""",
    
    AgentType.COMPANION: """You are a helpful AI companion running locally for privacy.
Your role: Conversational assistance with personality.
Output format: Natural, friendly dialogue.
Remember context, show empathy, be proactive.""",
}


# Natural language → Agent prompt translation templates
PROMPT_TEMPLATES = {
    AgentType.RESEARCHER: {
        "user_query": "{query}",
        "system_addon": "\nFocus on: {focus_areas}\nTime range: {time_range}",
        "focus_keywords": ["research", "find", "investigate", "learn about", "what is"],
    },
    
    AgentType.CODER: {
        "user_query": "Task: {query}\n\nRequirements:\n{requirements}\n\nLanguage: {language}",
        "system_addon": "\nCode style: {style}\nFrameworks: {frameworks}",
        "focus_keywords": ["code", "implement", "create", "build", "write", "function"],
    },
    
    AgentType.ARCHITECT: {
        "user_query": "Design request: {query}\n\nConstraints:\n{constraints}\n\nScale: {scale}",
        "system_addon": "\nArchitecture: {pattern}\nTech stack: {stack}",
        "focus_keywords": ["design", "architecture", "structure", "system", "plan"],
    },
    
    AgentType.ANALYST: {
        "user_query": "Analysis task: {query}\n\nData: {data_description}\n\nGoal: {goal}",
        "system_addon": "\nMetrics: {metrics}\nVisualization: {viz_type}",
        "focus_keywords": ["analyze", "compare", "evaluate", "assess", "metrics"],
    },
    
    AgentType.WRITER: {
        "user_query": "Writing task: {query}\n\nAudience: {audience}\n\nTone: {tone}",
        "system_addon": "\nLength: {length}\nFormat: {format}",
        "focus_keywords": ["write", "document", "explain", "describe", "summarize"],
    },
    
    AgentType.VISION: {
        "user_query": "Image analysis: {query}\n\n[Image attached]\n\nFocus: {focus}",
        "system_addon": "\nExtract: {extract_what}",
        "focus_keywords": ["see", "look at", "analyze image", "screenshot", "visual"],
    },
    
    AgentType.COMPANION: {
        "user_query": "{query}",
        "system_addon": "\nMood: {user_mood}\nContext: {recent_context}",
        "focus_keywords": ["chat", "help", "tell me", "think", "remember"],
    },
}


# Cost tracking (per 1M tokens)
SERVICE_COSTS = {
    CloudService.GEMINI: {"input": 0.075, "output": 0.30},
    CloudService.GPT: {"input": 10.0, "output": 30.0},
    CloudService.CLAUDE: {"input": 3.0, "output": 15.0},
    CloudService.PERPLEXITY: {"input": 1.0, "output": 1.0},
    CloudService.LOCAL: {"input": 0.0, "output": 0.0},
}


def get_agent_config(agent_type: AgentType) -> dict:
    """
    Get complete configuration for an agent.
    
    Args:
        agent_type: The type of agent
        
    Returns:
        Configuration dictionary
    """
    service = AGENT_SERVICE_MAP[agent_type]
    
    return {
        "agent_type": agent_type.value,
        "service": service.value,
        "service_config": SERVICE_CONFIG[service],
        "system_prompt": AGENT_SYSTEM_PROMPTS[agent_type],
        "prompt_template": PROMPT_TEMPLATES[agent_type],
        "cost_per_1m": SERVICE_COSTS[service],
    }


def detect_agent_from_query(query: str) -> AgentType:
    """
    Detect which agent type is most appropriate for a query.
    
    Args:
        query: User's natural language request
        
    Returns:
        Best matching AgentType
    """
    query_lower = query.lower()
    
    # Score each agent type
    scores = {agent: 0 for agent in AgentType}
    
    for agent_type, template in PROMPT_TEMPLATES.items():
        keywords = template["focus_keywords"]
        for keyword in keywords:
            if keyword in query_lower:
                scores[agent_type] += 1
    
    # Return highest scoring agent, default to COMPANION
    best_agent = max(scores, key=scores.get)
    return best_agent if scores[best_agent] > 0 else AgentType.COMPANION


if __name__ == "__main__":
    # Test agent detection
    test_queries = [
        "Research the latest AI trends",
        "Write a Python function to parse JSON",
        "Design a microservices architecture",
        "Analyze this sales data",
        "Help me understand quantum physics",
    ]
    
    print("=== Agent Detection Test ===\n")
    for query in test_queries:
        agent = detect_agent_from_query(query)
        config = get_agent_config(agent)
        print(f"Query: {query}")
        print(f"→ Agent: {agent.value}")
        print(f"→ Service: {config['service']}")
        print(f"→ Model: {config['service_config']['model']}")
        print()
