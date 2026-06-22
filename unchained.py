"""
Unchained — A complete agentic AI framework in one file.
No LangChain. No bloat. Just agents that work.

Dependencies: requests, pydantic
Usage:
    from unchained import Agent, tool
    @tool
    def search(query: str) -> str:
        '''Search the web.'''
        return f"Results for: {query}"
    agent = Agent(name="researcher", tools=[search])
    response = agent.run("Find me the latest AI news")
"""
from __future__ import annotations
import inspect, json, math, re
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Type
import requests
from pydantic import BaseModel

__version__ = "0.1.0"
__all__ = ["Agent", "tool", "Memory", "RAG", "Router", "LLM", "structured_output", "create_agent"]

# ── TOOL SYSTEM ──────────────────────────────────────────────

@dataclass
class Tool:
    """A callable tool with auto-generated schema."""
    name: str
    description: str
    function: Callable
    parameters: Dict[str, Any] = field(default_factory=dict)

    def to_schema(self) -> dict:
        """Convert to OpenAI-compatible function schema."""
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": self.parameters,
                    "required": [k for k, v in self.parameters.items()
                                 if "default" not in v],
                },
            },
        }

    def __call__(self, **kwargs) -> Any:
        return self.function(**kwargs)


def tool(func: Callable) -> Tool:
    """Decorator to register a function as an agent tool.

    Example:
        @tool
        def calculator(expression: str) -> str:
            '''Evaluate a math expression.'''
            return str(eval(expression))
    """
    sig = inspect.signature(func)
    hints = func.__annotations__
    type_map = {str: "string", int: "integer", float: "number",
                bool: "boolean", list: "array", dict: "object"}
    params = {}
    for name, param in sig.parameters.items():
        if name == "return":
            continue
        ptype = hints.get(name, str)
        params[name] = {"type": type_map.get(ptype, "string"),
                        "description": f"Parameter: {name}"}
        if param.default is not inspect.Parameter.empty:
            params[name]["default"] = param.default
    return Tool(name=func.__name__, description=(func.__doc__ or "").strip(),
                function=func, parameters=params)


# ── LLM BACKENDS ─────────────────────────────────────────────

class LLM:
    """Unified LLM interface. Supports OpenAI, Anthropic, and Ollama."""

    DEFAULTS = {
        "openai": ("gpt-4o-mini", "https://api.openai.com/v1"),
        "anthropic": ("claude-3-5-haiku-20241022", "https://api.anthropic.com"),
        "ollama": ("llama3.2", "http://localhost:11434"),
        "nvidia": ("nvidia/llama-3.1-nemotron-ultra-253b-v1", "https://integrate.api.nvidia.com/v1"),
    }

    def __init__(self, provider: str = "openai", model: Optional[str] = None,
                 api_key: Optional[str] = None, base_url: Optional[str] = None,
                 temperature: float = 0.7, max_tokens: int = 4096):
        self.provider = provider.lower()
        self.temperature, self.max_tokens, self.api_key = temperature, max_tokens, api_key
        default_model, default_url = self.DEFAULTS.get(self.provider, ("", ""))
        self.model = model or default_model
        self.base_url = base_url or default_url

    def chat(self, messages: List[dict], tools: Optional[List[dict]] = None,
             response_format: Optional[dict] = None) -> dict:
        """Send messages and return response with potential tool calls."""
        dispatch = {"openai": self._openai, "anthropic": self._anthropic,
                    "ollama": self._ollama, "nvidia": self._openai}
        if self.provider not in dispatch:
            raise ValueError(f"Unknown provider: {self.provider}")
        return dispatch[self.provider](messages, tools, response_format)

    def _openai(self, messages, tools, response_format) -> dict:
        headers = {"Authorization": f"Bearer {self.api_key}",
                   "Content-Type": "application/json"}
        payload = {"model": self.model, "messages": messages,
                   "temperature": self.temperature, "max_tokens": self.max_tokens}
        if tools:
            payload["tools"], payload["tool_choice"] = tools, "auto"
        if response_format:
            payload["response_format"] = response_format
        resp = requests.post(f"{self.base_url}/chat/completions",
                             headers=headers, json=payload, timeout=120)
        resp.raise_for_status()
        data = resp.json()
        msg = data["choices"][0]["message"]
        return {
            "content": msg.get("content", ""),
            "tool_calls": [{"name": tc["function"]["name"],
                           "arguments": json.loads(tc["function"]["arguments"])}
                          for tc in msg.get("tool_calls", [])],
            "usage": data.get("usage", {}),
        }

    def _anthropic(self, messages, tools, response_format) -> dict:
        headers = {"x-api-key": self.api_key, "anthropic-version": "2023-06-01",
                   "Content-Type": "application/json"}
        system, filtered = "", []
        for m in messages:
            if m["role"] == "system":
                system = m["content"]
            else:
                filtered.append(m)
        payload = {"model": self.model, "max_tokens": self.max_tokens,
                   "messages": filtered}
        if system:
            payload["system"] = system
        if tools:
            payload["tools"] = [{"name": t["function"]["name"],
                                 "description": t["function"]["description"],
                                 "input_schema": t["function"]["parameters"]}
                                for t in tools]
        resp = requests.post(f"{self.base_url}/v1/messages",
                             headers=headers, json=payload, timeout=120)
        resp.raise_for_status()
        data = resp.json()
        content, tool_calls = "", []
        for block in data.get("content", []):
            if block["type"] == "text":
                content += block["text"]
            elif block["type"] == "tool_use":
                tool_calls.append({"name": block["name"], "arguments": block["input"]})
        return {"content": content, "tool_calls": tool_calls,
                "usage": data.get("usage", {})}

    def _ollama(self, messages, tools, response_format) -> dict:
        payload = {"model": self.model, "messages": messages, "stream": False}
        if tools:
            payload["tools"] = tools
        if response_format:
            payload["format"] = "json"
        resp = requests.post(f"{self.base_url}/api/chat", json=payload, timeout=300)
        resp.raise_for_status()
        data = resp.json()
        msg = data.get("message", {})
        tool_calls = [{"name": tc.get("function", {}).get("name", ""),
                       "arguments": tc.get("function", {}).get("arguments", {})}
                      for tc in msg.get("tool_calls", [])]
        return {"content": msg.get("content", ""), "tool_calls": tool_calls,
                "usage": {"total_tokens": data.get("eval_count", 0)}}


# ── MEMORY ───────────────────────────────────────────────────

class Memory:
    """Sliding window memory with summary compression."""

    def __init__(self, max_messages: int = 20, llm: Optional[LLM] = None):
        self.max_messages = max_messages
        self.messages: List[dict] = []
        self.summary: str = ""
        self.llm = llm

    def add(self, role: str, content: str):
        self.messages.append({"role": role, "content": content})
        if len(self.messages) > self.max_messages:
            self._compress()

    def _compress(self):
        """Compress oldest messages into a summary."""
        half = self.max_messages // 2
        overflow = self.messages[:len(self.messages) - half]
        self.messages = self.messages[len(overflow):]
        if not self.llm:
            self.summary += "\n".join(f"{m['role']}: {m['content'][:100]}"
                                      for m in overflow)
            return
        context = "\n".join(f"{m['role']}: {m['content']}" for m in overflow)
        result = self.llm.chat([
            {"role": "system", "content": "Summarize this conversation concisely."},
            {"role": "user", "content": context},
        ])
        self.summary = result["content"]

    def get_messages(self, system_prompt: str = "") -> List[dict]:
        """Get full message history with system prompt and summary."""
        msgs = []
        if system_prompt or self.summary:
            sys_content = system_prompt
            if self.summary:
                sys_content += f"\n\n[Previous context]: {self.summary}"
            msgs.append({"role": "system", "content": sys_content})
        msgs.extend(self.messages)
        return msgs

    def clear(self):
        self.messages, self.summary = [], ""


# ── MINIMAL RAG (TF-IDF + Cosine — no vector DB needed) ─────

class RAG:
    """Minimal retrieval-augmented generation using TF-IDF + cosine similarity."""

    def __init__(self):
        self.documents: List[str] = []
        self.metadata: List[dict] = []
        self._idf: Dict[str, float] = {}
        self._tfidf_matrix: List[Dict[str, float]] = []

    def add(self, text: str, metadata: Optional[dict] = None):
        """Add a document to the knowledge base."""
        self.documents.append(text)
        self.metadata.append(metadata or {})
        self._rebuild_index()

    def add_many(self, texts: List[str], metadatas: Optional[List[dict]] = None):
        """Batch add documents."""
        self.documents.extend(texts)
        self.metadata.extend(metadatas or [{}] * len(texts))
        self._rebuild_index()

    def _tokenize(self, text: str) -> List[str]:
        return re.findall(r'\b\w+\b', text.lower())

    def _rebuild_index(self):
        n = len(self.documents)
        df = defaultdict(int)
        tf_docs = []
        for doc in self.documents:
            tokens = self._tokenize(doc)
            tf = defaultdict(int)
            for t in tokens:
                tf[t] += 1
            max_tf = max(tf.values()) if tf else 1
            tf = {k: v / max_tf for k, v in tf.items()}
            tf_docs.append(tf)
            for t in set(tokens):
                df[t] += 1
        self._idf = {t: math.log((1 + n) / (1 + freq)) + 1 for t, freq in df.items()}
        self._tfidf_matrix = [
            {t: freq * self._idf.get(t, 0) for t, freq in tf.items()}
            for tf in tf_docs
        ]

    def search(self, query: str, top_k: int = 3) -> List[dict]:
        """Retrieve top-k most relevant documents."""
        if not self.documents:
            return []
        tokens = self._tokenize(query)
        query_tf = defaultdict(int)
        for t in tokens:
            query_tf[t] += 1
        max_tf = max(query_tf.values()) if query_tf else 1
        query_vec = {t: (v / max_tf) * self._idf.get(t, 0)
                     for t, v in query_tf.items()}
        scores = []
        for i, doc_vec in enumerate(self._tfidf_matrix):
            all_terms = set(list(query_vec.keys()) + list(doc_vec.keys()))
            dot = sum(query_vec.get(t, 0) * doc_vec.get(t, 0) for t in all_terms)
            mag_q = math.sqrt(sum(v ** 2 for v in query_vec.values())) or 1
            mag_d = math.sqrt(sum(v ** 2 for v in doc_vec.values())) or 1
            scores.append((dot / (mag_q * mag_d), i))
        scores.sort(reverse=True)
        return [{"text": self.documents[idx], "score": round(s, 4),
                 "metadata": self.metadata[idx]}
                for s, idx in scores[:top_k] if s > 0]


# ── STRUCTURED OUTPUT ────────────────────────────────────────

def structured_output(llm: LLM, prompt: str, schema: Type[BaseModel],
                      system: str = "") -> BaseModel:
    """Get LLM response conforming to a Pydantic schema."""
    schema_json = json.dumps(schema.model_json_schema(), indent=2)
    full_prompt = (f"{prompt}\n\nRespond ONLY with valid JSON matching this "
                   f"schema:\n{schema_json}")
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": full_prompt})
    result = llm.chat(messages, response_format={"type": "json_object"})
    return schema.model_validate(json.loads(result["content"]))


# ── AGENT ────────────────────────────────────────────────────

class Agent:
    """The core agent. Think → Act → Observe → Repeat."""

    def __init__(self, name: str = "agent",
                 system_prompt: str = "You are a helpful AI assistant.",
                 llm: Optional[LLM] = None, tools: Optional[List[Tool]] = None,
                 memory: Optional[Memory] = None, rag: Optional[RAG] = None,
                 max_iterations: int = 10, verbose: bool = False):
        self.name = name
        self.system_prompt = system_prompt
        self.llm = llm or LLM()
        self.tools = {t.name: t for t in (tools or [])}
        self.memory = memory or Memory(llm=self.llm)
        self.rag = rag
        self.max_iterations = max_iterations
        self.verbose = verbose
        self._total_tokens = 0

    def run(self, user_input: str) -> str:
        """Run the agent on user input. Returns final response."""
        augmented = user_input
        if self.rag:
            results = self.rag.search(user_input)
            if results:
                context = "\n\n".join(f"[Source]: {r['text']}" for r in results)
                augmented = f"Context:\n{context}\n\nUser question: {user_input}"

        self.memory.add("user", augmented)
        tool_schemas = [t.to_schema() for t in self.tools.values()] or None

        for i in range(self.max_iterations):
            messages = self.memory.get_messages(self.system_prompt)
            result = self.llm.chat(messages, tools=tool_schemas)
            self._total_tokens += result.get("usage", {}).get("total_tokens", 0)

            if self.verbose:
                mode = "tool_call" if result["tool_calls"] else "response"
                print(f"  [{self.name}] Iteration {i+1}: {mode}")

            if not result["tool_calls"]:
                response = result["content"]
                self.memory.add("assistant", response)
                return response

            for tc in result["tool_calls"]:
                name, args = tc["name"], tc["arguments"]
                if name not in self.tools:
                    tool_result = f"Error: Tool '{name}' not found."
                else:
                    try:
                        tool_result = str(self.tools[name](**args))
                    except Exception as e:
                        tool_result = f"Error executing {name}: {e}"
                if self.verbose:
                    print(f"    Tool: {name}({args}) -> {tool_result[:100]}...")
                self.memory.add("assistant", f"[Calling tool: {name}({args})]")
                self.memory.add("user", f"[Tool result]: {tool_result}")

        return "Max iterations reached. Please refine your query."

    @property
    def token_usage(self) -> int:
        return self._total_tokens


# ── MULTI-AGENT ROUTER ───────────────────────────────────────

class Router:
    """Route queries to specialized agents based on intent."""

    def __init__(self, agents: List[Agent], llm: Optional[LLM] = None):
        self.agents = {a.name: a for a in agents}
        self.llm = llm or LLM()

    def route(self, user_input: str) -> str:
        """Determine best agent and delegate."""
        descriptions = "\n".join(f"- {n}: {a.system_prompt[:100]}"
                                 for n, a in self.agents.items())
        result = self.llm.chat([
            {"role": "system", "content": "You are a routing agent. Reply with ONLY the agent name."},
            {"role": "user", "content": f"Agents:\n{descriptions}\n\nQuery: {user_input}\n\nBest agent name:"},
        ])
        chosen = result["content"].strip().lower()
        for name in self.agents:
            if name.lower() in chosen or chosen in name.lower():
                return self.agents[name].run(user_input)
        return list(self.agents.values())[0].run(user_input)

    def run_all(self, user_input: str) -> Dict[str, str]:
        """Run ALL agents and collect results (for multi-agent synthesis)."""
        return {name: agent.run(user_input) for name, agent in self.agents.items()}


# ── CONVENIENCE ──────────────────────────────────────────────

def create_agent(name: str = "assistant", instructions: str = "You are a helpful assistant.",
                 tools: Optional[List[Tool]] = None, provider: str = "openai",
                 model: Optional[str] = None, api_key: Optional[str] = None, **kw) -> Agent:
    """One-liner agent creation."""
    return Agent(name=name, system_prompt=instructions,
                 llm=LLM(provider=provider, model=model, api_key=api_key),
                 tools=tools, **kw)
