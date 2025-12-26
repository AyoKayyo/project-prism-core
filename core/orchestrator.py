"""
Smart Orchestrator - Routes user requests to appropriate specialized agents

Translates natural language to agent-specific formats and manages cloud API calls.
"""

import os
from typing import Dict, Any, Optional
from enum import Enum

from config.agent_services import (
    AgentType,
    CloudService,
    get_agent_config,
    detect_agent_from_query,
    AGENT_SERVICE_MAP,
)
from utils.secure_store import SecureStore


class SmartOrchestrator:
    """
    Intelligent task router that:
    1. Detects which specialized agent to use
    2. Translates natural language to service-specific prompts
    3. Routes to appropriate cloud service
    4. Tracks costs and enforces budgets
    """
    
    def __init__(self, mcp=None):
        """
        Initialize orchestrator.
        
        Args:
            mcp: Main Control Program instance (for safety checks)
        """
        self.mcp = mcp
        self.agents = {}  # Lazy-loaded agent instances
        self._init_api_clients()
    
    def _init_api_clients(self):
        """Initialize API clients for cloud services."""
        # Import on-demand to avoid dependency issues
        try:
            import google.generativeai as genai
            api_key = SecureStore.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")
            if api_key:
                genai.configure(api_key=api_key)
                self.gemini = genai.GenerativeModel('gemini-2.0-flash-exp')
            else:
                self.gemini = None
        except ImportError:
            self.gemini = None
        
        # Add other service clients as needed
        self.anthropic = None  # TODO: Initialize Claude
        self.openai = None     # TODO: Initialize GPT
        self.perplexity = None # TODO: Initialize Perplexity
    
    def route_task(self, user_query: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Main routing function.
        
        Args:
            user_query: Natural language request from user
            context: Optional context (conversation history, user prefs, etc.)
            
        Returns:
            Response dictionary with result and metadata
        """
        context = context or {}
        
        # Step 1: Detect which agent to use
        agent_type = detect_agent_from_query(user_query)
        print(f"🎯 [Orchestrator] Routed to: {agent_type.value}")
        
        # Step 2: Get agent configuration
        config = get_agent_config(agent_type)
        
        # Step 3: Check if service is available
        service = CloudService(config['service'])
        if not self._is_service_available(service):
            # Fallback to local
            print(f"⚠️ [Orchestrator] {service.value} unavailable, using local")
            agent_type = AgentType.COMPANION
            config = get_agent_config(agent_type)
        
        # Step 4: Translate query to agent-specific prompt
        formatted_prompt = self._translate_prompt(user_query, agent_type, context)
        
        # Step 5: Get MCP approval (if applicable)
        if self.mcp:
            # TODO: Check safety tier for this action
            pass
        
        # Step 6: Execute via appropriate service
        response = self._execute_on_service(
            service=CloudService(config['service']),
            system_prompt=config['system_prompt'],
            user_prompt=formatted_prompt,
            model_config=config['service_config']
        )
        
        # Step 7: Track costs
        cost = self._calculate_cost(response, config['cost_per_1m'])
        
        return {
            "agent": agent_type.value,
            "service": config['service'],
            "model": config['service_config']['model'],
            "response": response['text'],
            "cost_usd": cost,
            "tokens": response.get('tokens', {}),
        }
    
    def _is_service_available(self, service: CloudService) -> bool:
        """Check if a cloud service is configured and available."""
        if service == CloudService.LOCAL:
            return True  # Always available
        elif service == CloudService.GEMINI:
            return self.gemini is not None
        elif service == CloudService.CLAUDE:
            return self.anthropic is not None
        elif service == CloudService.GPT:
            return self.openai is not None
        elif service == CloudService.PERPLEXITY:
            return self.perplexity is not None
        return False
    
    def _translate_prompt(
        self,
        user_query: str,
        agent_type: AgentType,
        context: Dict[str, Any]
    ) -> str:
        """
        Translate natural language to agent-specific format.
        
        This is where the magic happens - converting casual English
        to properly formatted prompts for each specialized agent.
        """
        config = get_agent_config(agent_type)
        template = config['prompt_template']
        
        # Extract parameters from query and context
        params = {
            "query": user_query,
            "focus_areas": context.get("focus", "general"),
            "time_range": context.get("time_range", "recent"),
            "requirements": context.get("requirements", "Follow best practices"),
            "language": context.get("language", "Python"),
            "style": context.get("code_style", "PEP 8"),
            "frameworks": context.get("frameworks", "standard library"),
            "constraints": context.get("constraints", "None specified"),
            "scale": context.get("scale", "medium"),
            "pattern": context.get("architecture", "microservices"),
            "stack": context.get("tech_stack", "modern"),
            "data_description": context.get("data", ""),
            "goal": context.get("goal", "insights"),
            "metrics": context.get("metrics", "standard"),
            "viz_type": context.get("visualization", "auto"),
            "audience": context.get("audience", "general"),
            "tone": context.get("tone", "professional"),
            "length": context.get("length", "medium"),
            "format": context.get("format", "markdown"),
            "focus": context.get("image_focus", "comprehensive"),
            "extract_what": context.get("extract", "all notable elements"),
            "user_mood": context.get("mood", "neutral"),
            "recent_context": context.get("recent_context", ""),
        }
        
        # Format the prompt
        try:
            formatted = template['user_query'].format(**params)
            if context.get("detailed"):
                formatted += template.get('system_addon', '').format(**params)
        except KeyError:
            # Fallback to simple format if parameters missing
            formatted = user_query
        
        return formatted
    
    def _execute_on_service(
        self,
        service: CloudService,
        system_prompt: str,
        user_prompt: str,
        model_config: Dict
    ) -> Dict[str, Any]:
        """
        Execute request on specified cloud service.
        
        Args:
            service: Which service to use
            system_prompt: Agent's system instructions
            user_prompt: Formatted user request
            model_config: Service-specific configuration
            
        Returns:
            Response dictionary with text and token counts
        """
        print(f"☁️ [Orchestrator] Calling {service.value} ({model_config['model']})")
        
        if service == CloudService.GEMINI and self.gemini:
            try:
                # Gemini API call
                full_prompt = f"{system_prompt}\n\n{user_prompt}"
                response = self.gemini.generate_content(
                    full_prompt,
                    generation_config={
                        "temperature": model_config['temperature'],
                        "max_output_tokens": model_config['max_tokens'],
                    }
                )
                return {
                    "text": response.text,
                    "tokens": {
                        "input": len(full_prompt.split()),  # Rough estimate
                        "output": len(response.text.split()),
                    }
                }
            except Exception as e:
                print(f"❌ [Orchestrator] Gemini error: {e}")
                return {"text": f"Error: {str(e)}", "tokens": {}}
        
        elif service == CloudService.LOCAL:
            # Use local Ollama
            try:
                from langchain_ollama import ChatOllama
                llm = ChatOllama(model=model_config['model'])
                response = llm.invoke(f"{system_prompt}\n\n{user_prompt}")
                return {
                    "text": response.content,
                    "tokens": {
                        "input": len(user_prompt.split()),
                        "output": len(response.content.split()),
                    }
                }
            except Exception as e:
                print(f"❌ [Orchestrator] Local error: {e}")
                return {"text": f"Error: {str(e)}", "tokens": {}}
        
        # TODO: Add Claude, GPT, Perplexity implementations
        else:
            return {
                "text": f"Service {service.value} not yet implemented",
                "tokens": {}
            }
    
    def _calculate_cost(self, response: Dict, cost_per_1m: Dict) -> float:
        """Calculate API cost in USD."""
        tokens = response.get('tokens', {})
        input_tokens = tokens.get('input', 0)
        output_tokens = tokens.get('output', 0)
        
        input_cost = (input_tokens / 1_000_000) * cost_per_1m['input']
        output_cost = (output_tokens / 1_000_000) * cost_per_1m['output']
        
        return round(input_cost + output_cost, 6)


if __name__ == "__main__":
    # Test orchestrator
    print("=== Testing Smart Orchestrator ===\n")
    
    orchestrator = SmartOrchestrator()
    
    # Test query
    result = orchestrator.route_task(
        "Research the latest developments in quantum computing",
        context={"time_range": "last 6 months"}
    )
    
    print(f"\nAgent: {result['agent']}")
    print(f"Service: {result['service']}")
    print(f"Model: {result['model']}")
    print(f"Cost: ${result['cost_usd']}")
    print(f"\nResponse preview: {result['response'][:200]}...")
