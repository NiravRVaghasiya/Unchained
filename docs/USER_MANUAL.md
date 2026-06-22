# 📖 Unchained — User Manual

> For first-time users and non-technical people who want to get started quickly.

---

## What is Unchained?

Unchained is a simple tool that lets you create **AI assistants** (called "agents") that can:
- Answer questions using AI models
- Search through your documents for answers
- Use custom tools you define (calculators, web search, databases, etc.)
- Work together as a team (multiple agents collaborating)

Think of it like building your own ChatGPT — but customized for YOUR tasks.

---

## Prerequisites (What You Need)

| Requirement | Why | How to Get It |
|---|---|---|
| **Python 3.9+** | Unchained is written in Python | [python.org/downloads](https://python.org/downloads) |
| **Ollama** (optional) | Run AI models for FREE on your computer | [ollama.com](https://ollama.com) |
| **OpenAI API key** (optional) | Use GPT-4 if you prefer cloud | [platform.openai.com](https://platform.openai.com) |

> 💡 **Zero-cost option**: Use Ollama (free, runs locally on your computer). No API keys, no bills.

---

## Installation (5 minutes)

### Step 1: Install Unchained

Open your terminal (Command Prompt on Windows, Terminal on Mac/Linux):

```bash
git clone https://github.com/<username>/unchained.git
cd unchained 
pip install -e .
```

### Step 2: Install a free AI model (recommended)

```bash
# Install Ollama from https://ollama.com, then:
ollama pull llama3.2
```

This downloads a free AI model (~4GB) that runs on your computer. No internet needed after download.

### Step 3: Verify it works

```bash
python -c "from unchained import Agent; print('Unchained ready!')"
```

If you see "Unchained ready!" — you're set! 🎉

---

## Your First Agent (2 minutes)

Create a file called `my_agent.py`:

```python
from unchained import Agent, LLM

# Create an agent that uses free local AI
agent = Agent(
    name="my_assistant",
    system_prompt="You are a helpful assistant that explains things simply.",
    llm=LLM(provider="ollama", model="llama3.2"),
)

# Ask it something
response = agent.run("Explain what machine learning is in 3 sentences")
print(response)
```

Run it:
```bash
python my_agent.py
```

**That's it!** You just built your first AI agent.

---

## Adding Tools (Make Your Agent DO Things)

Agents become powerful when they can use tools:

```python
from unchained import Agent, tool, LLM

@tool
def calculator(expression: str) -> str:
    """Calculate a math expression."""
    return str(eval(expression))

@tool
def get_weather(city: str) -> str:
    """Get current weather for a city."""
    # Replace with real API call
    return f"Weather in {city}: 22°C, sunny"

agent = Agent(
    name="smart_assistant",
    system_prompt="You help with math and weather questions. Use tools when needed.",
    llm=LLM(provider="ollama"),
    tools=[calculator, get_weather],
)

print(agent.run("What's 15% of 847?"))
print(agent.run("What's the weather in Warsaw?"))
```

The agent automatically knows WHEN to use each tool based on the question.

---

## Adding Knowledge (RAG — Document Q&A)

Make your agent answer questions from YOUR documents:

```python
from unchained import Agent, RAG, LLM

# Create a knowledge base
knowledge = RAG()
knowledge.add("Our company was founded in 2020 by Alice and Bob.")
knowledge.add("We have 50 employees across 3 offices.")
knowledge.add("Our main product is a CRM tool for small businesses.")
knowledge.add("Revenue last year was $2.5 million.")

# Create an agent with this knowledge
agent = Agent(
    name="company_expert",
    system_prompt="Answer questions about our company using the provided context.",
    llm=LLM(provider="ollama"),
    rag=knowledge,
)

print(agent.run("Who founded the company?"))
# → "The company was founded in 2020 by Alice and Bob."

print(agent.run("How many employees do we have?"))
# → "The company has 50 employees across 3 offices."
```

---

## Using PickMyStack (Web Demo)

PickMyStack helps you choose the right AI tools for your project:

### Option A: Command line
```bash
cd examples/pickmystack
python app.py
```

### Option B: Web interface (prettier)
```bash
pip install streamlit
streamlit run examples/pickmystack/ui/app_ui.py
```

Then open http://localhost:8501 in your browser.

**How to use it:**
1. Describe what you want to build (e.g., "chatbot for my documentation")
2. Set your budget ($0 for free options)
3. Click "Analyze & Recommend"
4. Get a ranked list of framework recommendations with reasons

---

## Common Tasks — Quick Reference

### "I want to use GPT-4 instead of Ollama"

```python
from unchained import LLM

# Option 1: OpenAI
llm = LLM(provider="openai", api_key="sk-your-key-here")

# Option 2: Anthropic (Claude)
llm = LLM(provider="anthropic", api_key="sk-ant-your-key")
```

### "I want my agent to remember past conversations"

Memory is built-in! The agent remembers by default (last 20 messages). For longer memory:

```python
from unchained import Agent, Memory, LLM

agent = Agent(
    llm=LLM(provider="ollama"),
    memory=Memory(max_messages=50),  # Remember more
)
```

### "I want multiple agents working together"

```python
from unchained import Agent, Router, LLM

llm = LLM(provider="ollama")

research_agent = Agent(name="researcher", llm=llm,
    system_prompt="You find information and facts.")
writing_agent = Agent(name="writer", llm=llm,
    system_prompt="You write clear, engaging text.")

router = Router(agents=[research_agent, writing_agent], llm=llm)
print(router.route("Write a summary about renewable energy"))
```

### "I want structured output (JSON)"

```python
from unchained import LLM, structured_output
from pydantic import BaseModel

class MovieReview(BaseModel):
    title: str
    rating: float
    summary: str

llm = LLM(provider="ollama")
review = structured_output(llm, "Review the movie Inception", MovieReview)
print(review.title, review.rating)
```

---

## Choosing Your LLM Provider

| Provider | Cost | Quality | Speed | Best For |
|---|---|---|---|---|
| **Ollama** (local) | $0 | Good | Depends on hardware | Learning, prototyping, privacy |
| **OpenAI GPT-4o-mini** | ~$0.15/1M tokens | Great | Fast | Cheap cloud option |
| **OpenAI GPT-4o** | ~$2.50/1M tokens | Excellent | Fast | Best quality |
| **Anthropic Claude** | ~$3/1M tokens | Excellent | Fast | Long documents |

**Recommendation for beginners**: Start with Ollama (free), switch to cloud when you need better quality.

---

## Troubleshooting

### "ConnectionError: Cannot connect to Ollama"
```bash
# Make sure Ollama is running:
ollama serve
# Then in another terminal:
ollama pull llama3.2
```

### "ModuleNotFoundError: No module named 'unchained'"
```bash
# Make sure you installed it:
pip install -e .
# Or add the folder to your Python path
```

### "Agent doesn't use my tools"
- Make sure your tool has a clear docstring (this tells the AI what the tool does)
- Make sure the system_prompt mentions the capability

### "Responses are slow"
- Ollama speed depends on your hardware (GPU recommended)
- Try a smaller model: `LLM(provider="ollama", model="phi3")`
- Or use cloud: `LLM(provider="openai", model="gpt-4o-mini")`

---

## What's Next?

1. **Explore examples**: Look in `examples/` for more ideas
2. **Build your own tools**: Any Python function can become a tool
3. **Add your documents**: Use `RAG` to make agents answer from your files
4. **Deploy**: Host on Streamlit Cloud for free (see `examples/pickmystack/ui/README_DEPLOY.md`)

---

## Getting Help

- **GitHub Issues**: Report bugs or ask questions
- **Examples folder**: Every example is self-contained and runnable
- **Source code**: `unchained.py` is 417 lines — you can read the whole thing in 15 minutes

---

*Built for people who believe AI tools should be simple to use, not just simple to talk about.*
