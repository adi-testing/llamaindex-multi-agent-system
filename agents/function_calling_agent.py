"""
FunctionCallingAgentManager: A wrapper class for LlamaIndex's FunctionCallingAgent.

Flow:
1. Constructor (__init__) receives a list of tool objects
2. The constructor initializes:
   - self.tools (from parameters)
   - self.llm (from config)
   - self.agent (by calling _create_agent())
3. _create_agent() creates a FunctionCallingAgent with the tools and LLM
4. query() method processes user queries by delegating to the FunctionCallingAgent
   and handles any errors that might occur

The function calling approach differs from ReAct by using structured function 
definitions that the LLM can directly call, rather than using a reasoning-action loop.
This results in more predictable tool usage patterns when the task is well-defined.
"""

import logging 
from typing import List
import importlib

from llama_index.core.agent import FunctionCallingAgent
from llama_index.core.tools import BaseTool

from llm.local_llm import get_llm

logger = logging.getLogger(__name__)

class FunctionCallingAgentManager(FunctionCallingAgent):
    """Manager for creating and using Function Calling agents."""
    def __init__(self, tools: List[BaseTool]):
        # Get LLM settings from config
        config_vars = vars(importlib.import_module("config"))
        self.llm = get_llm(config_vars)
        self.tools = tools
        self.agent = self._create_agent()
    
    def _create_agent(self) -> FunctionCallingAgent:
        """Create a FunctionCalling agent with the configured tools."""
        logger.info("Creating FunctionCalling agent")
        return FunctionCallingAgent.from_tools(
            tools=self.tools,
            llm=self.llm,
            verbose=True,
        )
    
    def query(self, query_text: str) -> str:
        """Process a query using the Function Calling agent."""
        logger.info(f"Processing query with Function Calling agent: {query_text}")
        try:
            # Call the agent's query method to process the input
            response = self.agent.query(query_text)
            return str(response)
        except Exception as e:
            logger.error(f"Error processing query: {e}")
            return f"An error occurred: {str(e)}"
 