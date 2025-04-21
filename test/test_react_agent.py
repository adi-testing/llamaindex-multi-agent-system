# test_react_agent.py
import logging
from knowledge_base.vector_store import KnowledgeBase
from tools.calculator_tool import get_calculator_tool
from tools.python_info_tool import get_python_info_tool
from agents.react_agent import ReActAgentManager
from llama_index.core.settings import Settings

logging.basicConfig(level=logging.DEBUG)

# Disable OpenAI LLM
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