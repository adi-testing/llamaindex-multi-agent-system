# LlamaIndex Multi-Agent

This project demonstrates a multi-agent system built with LlamaIndex that uses a local LLM via LM Studio.

## Features

- **Multiple Agent Types**: Support for ReAct and Function Calling agents
- **Local LLM Integration**: Connect to local LLMs via API endpoints
- **RAG Capabilities**: Knowledge base with vector store for retrieving relevant information
- **Extensible Tool System**: Easily add new tools for agents to use
- **Interactive Mode**: Chat with agents in a command-line interface
- **Query Mode**: Run single queries for testing

## LM Studio Setup

1. Download and install LM Studio from [https://lmstudio.ai/](https://lmstudio.ai/)

2. In LM Studio:
   - Download a compatible model (recommended models below)
   - Start a local server by clicking on the "Local Server" tab
   - Select your model and click "Start Server"
   - The default server URL is `http://localhost:1234/v1`

### Recommended Models for LM Studio

Choose one of these models for best results with function calling and reasoning:
- Mistral 7B Instruct v0.2
- Llama 2 13B Chat
- Phi-2 2.7B
- Gemma 7B Instruct
- Mixtral 8x7B Instruct

For function calling specifically, these models typically work well:
- Hermes 2 Pro Mistral 7B
- Nous-Hermes 2 Mixtral 8x7B
- OpenHermes 2.5 Mistral 7B
- WizardLM 2 7B

## Setup

1. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install requirements:
   ```
   pip install -r requirements.txt
   ```

3. Ensure LM Studio is running with a local server before starting the application.

## Usage

Run the application with a specific agent type:

```
# Use ReAct agent (default)
python main.py --agent react

# Use Function Calling agent
python main.py --agent function

# Run with a specific query
python main.py --agent function --query "What is LlamaIndex?"

# Explicitly specify to use local LLM (default)
python main.py --llm local
```

In interactive mode, type any of these to exit:

exit
quit
bye

## Switching to OpenAI

If you want to use OpenAI instead of a local LLM:

1. Create a `.env` file with your API key:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

2. Run with the OpenAI option:
   ```
   python main.py --llm openai
   ```

## Troubleshooting

If you encounter issues with the local LLM:

1. Check that LM Studio server is running at http://localhost:1234/v1
2. Some models might not support function calling well - try a different model
3. For ReAct agent, ensure your model has good reasoning capabilities
4. Check the server logs in LM Studio for any specific errors
"""

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
