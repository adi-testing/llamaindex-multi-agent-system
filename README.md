# LlamaIndex Multi-Agent

A flexible and extensible framework for building and testing different agent architectures with LlamaIndex.

## Features

- **Multiple Agent Types**: Support for ReAct and Function Calling agents
- **Local LLM Integration**: Connect to local LLMs via API endpoints
- **RAG Capabilities**: Knowledge base with vector store for retrieving relevant information
- **Extensible Tool System**: Easily add new tools for agents to use
- **Interactive Mode**: Chat with agents in a command-line interface
- **Query Mode**: Run single queries for testing

## Setup

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/llamaindex-multi-agent.git
cd llamaindex-multi-agent

# Install in development mode
pip install -e .
```

### Configuration

```python
# For local LLM (e.g., using LM Studio)
LLM_TYPE = "lm_studio_local"
LOCAL_LLM_URL = "http://localhost:1234/v1"
LOCAL_LLM_MODEL = "mistral-7b-instruct-v0.3"

# For OpenAI (uncomment and add your key)
# LLM_TYPE = "openai"
# OPENAI_API_KEY = "your-api-key"
# OPENAI_LLM_MODEL = "gpt-3.5-turbo"
```
### Usage
```python
# Interactive mode with ReAct agent
python main.py --agent react

# Single query mode
python main.py --agent react --query "What is LlamaIndex?"
```
### Exit Commands

In interactive mode, type any of these to exit:

exit
quit
bye

## Components

Agents
- ReAct Agent: Uses reasoning-action loops, works with most LLMs
- Function Calling Agent: Uses structured function calls, requires LLMs with function calling support (Not working at the moment)

Tools
- Knowledge Base Tool: Retrieves information from the vector database
- Calculator Tool: Performs mathematical calculations
- Python Info Tool: Provides information about Python packages

## Notes
- The system has a 60-second timeout for queries to prevent infinite loops
- ReAct agents are recommended for local LLMs without function calling  capabilities
- Function Calling agents require models like GPT-3.5/4 or similar with function calling APIs

## Testing
```python
# Test ReAct agent
python test/test_react_agent.py

# Test Function Calling agent (requires supported LLM)
python test/test_function_calling_agent.py
```
