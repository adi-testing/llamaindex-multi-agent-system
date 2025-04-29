"""
Test script for the FunctionCallingAgentManager.

Flow:
1. Import required modules and configure logging
2. Disable OpenAI LLM to use local LLM instead
3. Set up tools:
   - Knowledge base tool for RAG capabilities
   - Calculator tool for math operations
   - Python info tool for Python-related queries
4. Create a FunctionCallingAgentManager instance, passing the list of tools
   (This triggers the constructor and initializes the agent)
5. Test the agent by sending several structured queries to demonstrate
   the direct function calling capability

The function calling approach excels at tasks with clear function needs,
where the LLM can directly identify which function to call without the
step-by-step reasoning used in ReAct agents.
"""

import logging
from llama_index.core.settings import Settings
from knowledge_base.vector_store import KnowledgeBase
from tools.calculator_tool import get_calculator_tool
from tools.python_info_tool import get_python_info_tool
from tools.weather_tool import get_weather_tool
from agents.function_calling_agent import FunctionCallingAgentManager

logging.basicConfig(level=logging.DEBUG)

# Disable the default OpenAI LLM to ensure local LLM is used
Settings.llm = None

# Set up tools
kb = KnowledgeBase()
kb.initialize()
kb_tool = kb.get_query_engine_tool()
calc_tool = get_calculator_tool()
python_tool = get_python_info_tool()
weather_tool = get_weather_tool()

# Create agent
agent = FunctionCallingAgentManager([kb_tool, calc_tool, python_tool, weather_tool])

# Test queries that highlight function calling capabilities
print("\n===== TESTING FUNCTION CALLING AGENT =====\n")

# Test 1: Direct calculator function usage
print("Test 1: Calculator Function")
response = agent.query("Calculate 1243 * 729 / 3.14")
print(f"Response: {response}\n")

# Test 2: Knowledge base lookup
print("Test 2: Knowledge Base Lookup")
response = agent.query("Explain what vector databases are and how they're used in RAG")
print(f"Response: {response}\n")

# Test 3: Python package information
print("Test 3: Python Package Information")
response = agent.query("What is the requests package in Python used for?")
print(f"Response: {response}\n")

# Test 4: Complex query requiring multiple tool selection
print("Test 4: Multi-tool Interaction")
response = agent.query("If I have a list of 5 numbers: 10, 20, 30, 40, 50, " +
                      "what's their average? Also, explain how I could use Python's " +
                      "statistics module to calculate this.")
print(f"Response: {response}\n")

# Test 5: Function selection with ambiguous query
print("Test 5: Function Selection Test")
response = agent.query("I need to understand how embeddings work in RAG systems " +
                      "and also calculate the dimensions if I use a 768-dimensional " +
                      "vector with 10,000 documents.")
print(f"Response: {response}")