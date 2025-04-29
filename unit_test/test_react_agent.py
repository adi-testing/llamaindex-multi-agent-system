"""
Test script for the ReActAgentManager.

Flow:
1. Import required modules and configure logging
2. Disable OpenAI LLM to use local LLM instead
3. Set up tools:
   - Knowledge base tool for RAG capabilities
   - Calculator tool for math operations
   - Python info tool for Python-related queries
4. Create a ReActAgentManager instance, passing the list of tools
   (This triggers the constructor and initializes the agent)
5. Test the agent by sending a query and printing the response

The -> str notation indicates the method returns a string.
"""

import logging
from knowledge_base.vector_store import KnowledgeBase
from tools.calculator_tool import get_calculator_tool
from tools.python_info_tool import get_python_info_tool
from agents.react_agent import ReActAgentManager
from llama_index.core.settings import Settings


logging.basicConfig(level=logging.DEBUG)

# Disable the default OpenAI LLM to ensure local LLM is used
Settings.llm = None

# Set up tools
kb = KnowledgeBase()
kb.initialize()
kb_tool = kb.get_query_engine_tool()
calc_tool = get_calculator_tool()
python_tool = get_python_info_tool()

# Create agent
agent = ReActAgentManager([kb_tool, calc_tool, python_tool])

# Test query
response_text = agent.query("What is RAG?")
print(f"Response: {response_text}")