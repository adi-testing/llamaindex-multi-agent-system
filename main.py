import os
import logging
import argparse
import signal
from contextlib import contextmanager
from typing import List, Dict, Any

from llama_index.core import Settings
from llama_index.core.tools import BaseTool
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

import config
from llm.local_llm import get_llm
from knowledge_base.vector_store import KnowledgeBase
from tools.calculator_tool import get_calculator_tool
from tools.python_info_tool import get_python_info_tool
from tools.weather_tool import get_weather_tool
from agents.react_agent import ReActAgentManager

# Set up logging
"""Set up logging configuration for the script."""
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Set up environment
def setup_environment():
    """Set up the environment and LlamaIndex settings."""
    # Configure LlamaIndex settings
    Settings.llm = None
    logger.info("Environment setup complete.")

def setup_tools() -> List[BaseTool]:
    """Set up the tools for the agent."""
    # Initialize knowledge base
    kb = KnowledgeBase()
    kb.initialize()
    kb_tool = kb.get_query_engine_tool()

    # Get function tools
    calculator_tool = get_calculator_tool()
    python_tool = get_python_info_tool()
    weather_tool = get_weather_tool()

    # Combine all tools into a list
    tools = [kb_tool, calculator_tool, python_tool, weather_tool]
    logger.info(f"Created {len(tools)} tools for the agent.")
    return tools

@contextmanager
def timeout(seconds):
    def handler(signum, frame):
        raise TimeoutError(f"Query processing timed out after {seconds} seconds")
    
    # Set the timeout handler
    signal.signal(signal.SIGALRM, handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        # Disable the alarm
        signal.alarm(0)

def run_demo(agent_type: str, query: str = None):
    """Run a demonstration of the specified agent type."""
    setup_environment()
    tools = setup_tools()

    if agent_type.lower() == "react":
        # Create ReAct agent
        agent_manager = ReActAgentManager(tools)
        agent_name = "React Agent"
    else:
        raise ValueError(f"Unknown agent type: {agent_type}")

    logger.info(f"Running demo with {agent_name}...")

    if query:
        # Process a single query
        response = agent_manager.query(query)
        print(f"Response: {response}")
    else:
        # Iterative mode
        print("Running in iterative mode. Type 'exit' to quit.")

        while True:
            query = input("\nEnter your query: ")
            if query.lower() in ["exit", "quit", "bye"]:
                print("Exiting...")
                break
            print("\nProcessing query...")
            try:
                with timeout(60):  # 60 second timeout
                    response = agent_manager.query(query)
                    print(f"\nResponse: {response}")
            except TimeoutError as e:
                print(f"\n{str(e)}")
                print("Moving on to the next query...")

def main():
    """Main entry point for the application."""
    parser = argparse.ArgumentParser(description="LlamaIndex Multi-Agent Demo")
    parser.add_argument(
        "--agent",
        choices=["react", "function"],
        default="react",
        help="Type of agent to use (react or function)"
    )
    parser.add_argument(
        "--query",
        type=str,
        help="Query to process (if not provided, interactive mode is enabled)"
    )
    parser.add_argument(
        "--llm",
        choices=["local", "openai"],
        default="local",
        help="LLM type to use (local or openai)"
    )
    
    args = parser.parse_args()
    
    # Override LLM type if specified
    if args.llm:
        config.LLM_TYPE = args.llm
        
    run_demo(args.agent, args.query)

if __name__ == "__main__":
    main()



