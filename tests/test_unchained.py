"""
Unit tests for Unchained core components.
Run: python -m pytest tests/ -v
"""
import pytest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from unchained import tool, Tool, Memory, RAG, LLM, Agent


# ─── Tool Tests ──────────────────────────────────────────────

class TestTool:
    def test_tool_decorator_creates_tool(self):
        @tool
        def greet(name: str) -> str:
            """Say hello."""
            return f"Hello, {name}!"

        assert isinstance(greet, Tool)
        assert greet.name == "greet"
        assert greet.description == "Say hello."
        assert "name" in greet.parameters

    def test_tool_execution(self):
        @tool
        def add(a: int, b: int) -> int:
            """Add two numbers."""
            return a + b

        result = add(a=3, b=5)
        assert result == 8

    def test_tool_schema_generation(self):
        @tool
        def search(query: str, limit: int) -> str:
            """Search for something."""
            return query

        schema = search.to_schema()
        assert schema["type"] == "function"
        assert schema["function"]["name"] == "search"
        assert "query" in schema["function"]["parameters"]["properties"]
        assert "limit" in schema["function"]["parameters"]["properties"]


# ─── Memory Tests ────────────────────────────────────────────

class TestMemory:
    def test_add_and_retrieve(self):
        mem = Memory(max_messages=10)
        mem.add("user", "Hello")
        mem.add("assistant", "Hi there!")

        messages = mem.get_messages("You are helpful.")
        assert len(messages) == 3  # system + 2 messages
        assert messages[0]["role"] == "system"
        assert messages[1]["content"] == "Hello"

    def test_compression_triggers(self):
        mem = Memory(max_messages=4)
        for i in range(10):
            mem.add("user", f"Message {i}")

        # Should have compressed
        assert len(mem.messages) <= 4
        assert mem.summary != ""

    def test_clear(self):
        mem = Memory()
        mem.add("user", "test")
        mem.clear()
        assert len(mem.messages) == 0
        assert mem.summary == ""


# ─── RAG Tests ───────────────────────────────────────────────

class TestRAG:
    def test_add_and_search(self):
        rag = RAG()
        rag.add("Python is a programming language created by Guido van Rossum")
        rag.add("JavaScript is used for web development")
        rag.add("Rust is known for memory safety")

        results = rag.search("programming language creator")
        assert len(results) > 0
        assert "Python" in results[0]["text"]

    def test_empty_search(self):
        rag = RAG()
        results = rag.search("anything")
        assert results == []

    def test_batch_add(self):
        rag = RAG()
        docs = ["Document one about artificial intelligence", "Document two about machine learning",
                "Document three about data science"]
        rag.add_many(docs)
        assert len(rag.documents) == 3

        results = rag.search("machine learning models")
        assert len(results) > 0

    def test_relevance_scoring(self):
        rag = RAG()
        rag.add("The quick brown fox jumped over the lazy dog")
        rag.add("Supervised learning transforms training data into predictions")
        rag.add("Neural networks have layers of neurons")
        rag.add("Convolutional networks process images with filters")

        results = rag.search("neural networks architecture")
        # Neural networks doc should be in top results
        assert len(results) > 0
        assert "neural" in results[0]["text"].lower()


# ─── LLM Tests (Mock) ───────────────────────────────────────

class TestLLM:
    def test_initialization_defaults(self):
        llm = LLM(provider="openai")
        assert llm.model == "gpt-4o-mini"
        assert "openai" in llm.base_url

    def test_ollama_defaults(self):
        llm = LLM(provider="ollama")
        assert llm.model == "llama3.2"
        assert "11434" in llm.base_url

    def test_custom_config(self):
        llm = LLM(provider="openai", model="gpt-4o",
                   temperature=0.2, max_tokens=2048)
        assert llm.model == "gpt-4o"
        assert llm.temperature == 0.2
        assert llm.max_tokens == 2048


# ─── Agent Tests (Integration — requires LLM) ───────────────

class TestAgentUnit:
    def test_agent_creation(self):
        agent = Agent(name="test", system_prompt="You are helpful.")
        assert agent.name == "test"
        assert agent.max_iterations == 10

    def test_agent_with_tools(self):
        @tool
        def echo(text: str) -> str:
            """Echo text back."""
            return text

        agent = Agent(name="test", tools=[echo])
        assert "echo" in agent.tools

    def test_agent_with_rag(self):
        rag = RAG()
        rag.add("Unchained is a minimal framework")
        agent = Agent(name="test", rag=rag)
        assert agent.rag is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
