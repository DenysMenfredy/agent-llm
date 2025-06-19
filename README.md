# Research Agent

A Python-based research agent powered by open-source LLMs that can search the web, analyze information, and generate comprehensive reports.

## Features

- 🔍 **Web Search**: Automated web searching using DuckDuckGo API
- 📊 **Information Summarization**: Intelligent text summarization and organization
- 🤖 **Local LLM Integration**: Uses Ollama for completely offline LLM inference
- 🔧 **Extensible Tool System**: Easy to add new capabilities
- 🎯 **Iterative Reasoning**: Agent can plan, execute, and refine research approaches

## Prerequisites

- Python 3.8+
- [uv](https://github.com/astral-sh/uv) package manager
- [Ollama](https://ollama.com/) for local LLM inference

## Installation

### 1. Install uv (if not already installed)

```bash
# On macOS and Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. Clone and setup the project

```bash
git clone <your-repo-url>
cd research-agent

# Create virtual environment and install dependencies
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install requests
```

### 3. Install and setup Ollama

```bash
# Install Ollama (visit https://ollama.com/download for other platforms)
curl -fsSL https://ollama.com/install.sh | sh

# Start Ollama server
ollama serve

# In another terminal, pull a model
ollama pull llama3.2

# Optional: For lower memory usage, try smaller models
ollama pull llama3.2:1b
```

## Project Structure

```
research-agent/
├── src/
│   ├── __init__.py
│   ├── agent.py          # ResearchAgent class
│   ├── llm.py           # OllamaLLM class
│   ├── tools.py         # Tool classes (WebSearchTool, SummaryTool)
│   └── utils.py         # Message dataclass and utilities
├── main.py              # Main application entry point
├── README.md
└── requirements.txt     # (optional, for non-uv users)
```

## Usage

### Basic Usage

```bash
# Make sure Ollama is running in another terminal
ollama serve

# Run the research agent
uv run python main.py
```

### Example Research Topics

The agent can help you research various topics:

- "Research the current state of renewable energy adoption globally"
- "What are the main challenges in artificial intelligence ethics?"
- "Explain the recent developments in quantum computing"
- "Analyze the impact of remote work on productivity"

### Programmatic Usage

```python
from src.llm import OllamaLLM
from src.agent import ResearchAgent

# Initialize components
llm = OllamaLLM(model="llama3.2")
agent = ResearchAgent(llm)

# Run research
result = agent.run("Your research topic here")
print(result)
```

## Configuration

### Changing the LLM Model

Edit the model parameter in `main.py` or when initializing `OllamaLLM`:

```python
# Use a different model
llm = OllamaLLM(model="llama3.1")

# Use a smaller model for faster inference
llm = OllamaLLM(model="llama3.2:1b")
```

### Available Models

Check available models:
```bash
ollama list
```

Popular options:
- `llama3.2` (8B parameters) - Good balance of performance and speed
- `llama3.2:1b` (1B parameters) - Faster, lower memory usage
- `llama3.1` (8B parameters) - Alternative model
- `mistral` (7B parameters) - Different model family

## Troubleshooting

### Common Issues

**1. "Cannot connect to Ollama"**
```bash
# Make sure Ollama is running
ollama serve
```

**2. "Model not found"**
```bash
# Check available models
ollama list

# Install the model you want
ollama pull llama3.2
```

**3. "HTTP 500 error"**
- Usually indicates model issues
- Try pulling the model again: `ollama pull llama3.2`
- Check if you have enough RAM (8B models need ~8GB RAM)

**4. Slow performance**
- Try a smaller model: `ollama pull llama3.2:1b`
- Reduce max_tokens in the agent configuration

### Debug Mode

The application includes built-in diagnostics that run automatically and will help identify common issues.

### Memory Requirements

- **llama3.2:1b**: ~2GB RAM
- **llama3.2** (8B): ~8GB RAM
- **llama3.1** (8B): ~8GB RAM

## Development

### Adding New Tools

1. Create a new tool class in `src/tools.py`:

```python
class YourNewTool(Tool):
    def execute(self, **kwargs) -> str:
        # Your tool logic here
        return "Tool result"
    
    def description(self) -> str:
        return "your_tool(param: str) - Description of what it does"
```

2. Register it in the `ResearchAgent` class:

```python
self.tools = {
    "web_search": WebSearchTool(),
    "summarize": SummaryTool(),
    "your_tool": YourNewTool()  # Add your tool here
}
```

## Dependencies

- `requests`: HTTP client for API calls
- `ollama`: Local LLM inference (via HTTP API)

## License

MIT License - feel free to use and modify as needed.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Support

If you encounter issues:

1. Check the troubleshooting section above
2. Ensure Ollama is properly installed and running
3. Verify you have sufficient system resources
4. Check that your model is properly installed with `ollama list`