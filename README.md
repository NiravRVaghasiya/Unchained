# 🤖 Unchained ### A complete agentic AI framework in one file. **No LangChain. No bloat. Just agents that work.** [![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/) [![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT) [![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff) [Features](#features) • [Quick Start](#quick-start) • [Examples](#examples) • [PickMyStack](#-pickmystack) • [Benchmarks](#benchmarks) • [Philosophy](#philosophy)

---

## The Problem

The AI framework landscape is **overwhelming**:

```
You want to build an agent...
├── LangChain? (200,000+ lines, 150+ dependencies)
├── LlamaIndex? (great for RAG, overkill for agents)
├── CrewAI? (multi-agent, but still maturing)
├── AutoGen? (complex, Microsoft-centric)
├── Semantic Kernel? (enterprise-heavy)
├── DSPy? (academic, steep learning curve)
└── ...47 more options released this week

```

**Unchained answers: What if you just... didn't need any of that?**

---

## Quick Start

```bash
git clone https://github.com/NiravRVaghasiya/Unchained.git
cd Unchained
pip install -e .

```

**Build an agent in 5 lines:**

```python
from unchained import Agent, tool, LLM

@tool
def search(query: str) -> str:
    """Search the web."""
    return f"Results for: {query}"  # Replace with real implementation

agent = Agent(name="assistant", tools=[search],
              llm=LLM(provider="ollama"))  # Free, local
print(agent.run("Find the latest AI news"))

```

**That's it.** No chains. No graphs. No abstractions. Just an agent.

---

## Features

| Feature | Lines | LangChain Equivalent |
| --- | --- | --- |
| 🔧 Tool calling with auto-schema | ~80 | `BaseTool`, `StructuredTool`, `@tool` |
| 🧠 Memory (sliding window + compression) | ~60 | `ConversationBufferWindowMemory` + `ConversationSummaryMemory` |
| 📚 RAG (TF-IDF + cosine, no vector DB) | ~70 | `VectorStoreRetriever` + `ChromaDB` + `HuggingFace embeddings` |
| 🤝 Multi-agent routing | ~50 | `AgentExecutor` + routing chains |
| 📋 Structured output (Pydantic) | ~40 | `PydanticOutputParser` + `OutputFixingParser` |
| 🔌 LLM backends (OpenAI, Anthropic, Ollama) | ~70 | `ChatOpenAI`, `ChatAnthropic`, `ChatOllama` |
| **Total** | **~400** | **200,000+** |

### Zero-Cost Stack

```python
# Runs 100% free on your machine
from unchained import Agent, LLM

agent = Agent(
    llm=LLM(provider="ollama", model="llama3.2"),  # Free
    # No API keys needed. No cloud. No bills.
)

```

---

## Examples

### 🔍 Web Researcher (30 lines)

```python
from unchained import Agent, tool, LLM
import requests

@tool
def web_search(query: str) -> str:
    """Search using DuckDuckGo."""
    resp = requests.get("https://api.duckduckgo.com/",
                        params={"q": query, "format": "json"})
    data = resp.json()
    return data.get("AbstractText") or "No results."

agent = Agent(name="researcher", tools=[web_search],
              llm=LLM(provider="ollama"))
print(agent.run("What is retrieval augmented generation?"))

```

### 💻 Code Assistant (25 lines)

```python
from unchained import Agent, tool, LLM

@tool
def run_code(code: str) -> str:
    """Execute Python code safely."""
    try:
        exec_globals = {}
        exec(code, {"__builtins__": {}}, exec_globals)
        return str(exec_globals)
    except Exception as e:
        return f"Error: {e}"

agent = Agent(name="coder", tools=[run_code],
              llm=LLM(provider="ollama"))
print(agent.run("Write code to find prime numbers under 50"))

```

### 🤝 Multi-Agent System (25 lines)

```python
from unchained import Agent, Router, LLM

llm = LLM(provider="ollama")

researcher = Agent(name="researcher", llm=llm,
    system_prompt="You research topics thoroughly.")
writer = Agent(name="writer", llm=llm,
    system_prompt="You write clear, engaging content.")
critic = Agent(name="critic", llm=llm,
    system_prompt="You provide constructive feedback.")

router = Router(agents=[researcher, writer, critic], llm=llm)
print(router.route("Write a blog post about AI agents"))

```

---

## 🎯 PickMyStack

**The flagship app built on Unchained** — an AI framework advisor that helps developers choose the right stack.

```bash
cd examples/pickmystack
python app.py

```

```
> Build a customer support chatbot, budget $0, solo developer

Analyzing with multi-agent evaluation pipeline...

┌─────────────────────────────────────────────────┐
│ #1: Unchained + Ollama + ChromaDB                │
│     Cost: $0/month | Fit: 95% | Complexity: Low │
├─────────────────────────────────────────────────┤
│ #2: LlamaIndex + GPT-4o-mini                    │
│     Cost: ~$15/month | Fit: 88%                 │
├─────────────────────────────────────────────────┤
│ #3: LangChain + Pinecone + GPT-4o              │
│     Cost: ~$120/month | Fit: 72%                │
└─────────────────────────────────────────────────┘

```

PickMyStack uses 4 specialized agents:

- **CostAgent** — estimates total cost of ownership
- **FitAgent** — scores framework match to requirements
- **TrendAgent** — evaluates community health and momentum
- **Synthesizer** — produces final ranked recommendation

---

## 🖥️ Web UI (Streamlit)

PickMyStack includes a polished Streamlit frontend:

```bash
pip install streamlit
streamlit run examples/pickmystack/ui/app_ui.py
```

Features:
- Natural language input + constraint selectors (budget, team size, priorities)
- Real-time progress bar as each agent evaluates
- Expandable detailed analysis from each specialist agent
- Works with Ollama (free) or cloud APIs
- Deployable to Streamlit Cloud / HuggingFace Spaces for free

---

## Benchmarks

```bash
python benchmarks/compare_frameworks.py

```

### Lines of Code (equivalent functionality)

| Task | Unchained | LangChain | CrewAI |
| --- | --- | --- | --- |
| Agent + Tool | 15 | 45 | 25 |
| Multi-Agent Router | 25 | 80 | 40 |
| RAG Pipeline | 20 | 60 | 50 |
| Structured Output | 10 | 35 | 30 |
| **Total Framework** | **~400** | **200K+** | **15K+** |

### Dependencies

| Framework | Direct Deps | Transitive Deps | Install Size |
| --- | --- | --- | --- |
| Unchained | 2 | ~10 | < 1 MB |
| LangChain | 15+ | 150+ | ~500 MB |
| CrewAI | 8+ | 80+ | ~200 MB |

---

## Philosophy

> *"Perfection is achieved, not when there is nothing more to add, but when there is nothing left to take away."* — Antoine de Saint-Exupery

### Why Unchained exists:

1. **You should understand your tools.** Can you read your framework's source in one sitting? With Unchained, yes.
2. **Most projects don't need LangChain.** If you're building a chatbot, RAG app, or multi-agent system — 400 lines is enough.
3. **Complexity is a choice, not a requirement.** Every abstraction layer is a debugging layer.
4. **$0 should be the default.** Unchained + Ollama = fully functional AI agent stack at zero cost.

### When NOT to use Unchained:

- You need 50+ pre-built integrations → use LangChain
- You need enterprise support contracts → use Semantic Kernel
- Your team already knows LangChain well → stay with what works

---

## Architecture

```
unchained.py (the whole framework)
│
├── Tool System        — @tool decorator, auto-schema generation
├── LLM Backends       — OpenAI, Anthropic, Ollama (unified interface)
├── Memory             — Sliding window + LLM-powered compression
├── RAG                — TF-IDF + cosine similarity (no vector DB)
├── Structured Output  — Pydantic schema enforcement
├── Agent              — Think → Act → Observe loop
└── Router             — Multi-agent delegation and synthesis

```

---

## Roadmap

- [x] **v0.1** — Core framework + PickMyStack MVP *(you are here)*
- [ ] **v0.2** — Streaming responses, async tool execution
- [ ] **v0.3** — Plugin system (community-contributed tools)
- [ ] **v0.4** — Persistent memory (SQLite-backed)
- [x] **v0.5** — Web UI (Streamlit dashboard) ✓
- [ ] **v1.0** — Production-ready, battle-tested

---

## Contributing

Unchained stays minimal by design. Contributions welcome for:

- 🐛 Bug fixes
- 📚 New examples (keep them under 50 lines!)
- 🧪 Test coverage
- 📖 Documentation
- 🔧 New LLM backend adapters

**Rule: **`unchained.py`** stays under 500 lines. Always.**

---

## License

MIT — do whatever you want with it.

---

 **Built with the belief that AI frameworks should be understood, not feared.** ⭐ Star this repo if you think simplicity wins.