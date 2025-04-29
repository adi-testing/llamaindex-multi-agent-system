"""
ReActAgentManager: A wrapper class for LlamaIndex's ReActAgent.

Flow:
1. Constructor (__init__) receives a list of tool objects
2. The constructor initializes:
   - self.tools (from parameters)
   - self.llm (from config)
   - self.agent (by calling _create_agent())
3. _create_agent() creates a ReActAgent with the tools and LLM
4. query() method processes user queries by delegating to the ReActAgent
   and handles any errors that might occur

The 'self' parameter in each method refers to the specific instance,
allowing each ReActAgentManager to maintain its own state.
"""

import logging
from typing import List
import importlib

from llama_index.core.agent import ReActAgent
from llama_index.core.tools import BaseTool

from config import LLM_TYPE
from llm.local_llm import get_llm

logger = logging.getLogger(__name__)

class ReActAgentManager:
    """Manager for creating and using ReAct agents."""
    
    def __init__(self, tools: List[BaseTool]):
        """Initialize the agent manager with tools."""
        self.tools = tools
        # Get LLM settings from config
        config_vars = vars(importlib.import_module("config"))
        self.llm = get_llm(config_vars)
        self.agent = self._create_agent()
        
    def _create_agent(self) -> ReActAgent:
        """Create a ReAct agent with the configured tools."""
        logger.info("Creating ReAct agent")
        return ReActAgent.from_tools(
            tools=self.tools,
            llm=self.llm,
            verbose=True,
            max_iterations=10,
        )
    
    def query(self, query_text: str) -> str:
        """Process a query using the ReAct agent."""
        logger.info(f"Processing query with ReAct agent: {query_text}")
        try:
            # Call the agent's query method to process the input
            response = self.agent.query(query_text)
            return str(response)
        except Exception as e:
            logger.error(f"Error processing query: {e}")
            return f"An error occurred: {str(e)}"