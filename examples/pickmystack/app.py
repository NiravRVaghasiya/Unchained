"""
PickMyStack — AI Framework Advisor
Built entirely on Unchained. The flagship demonstration app.

Multi-agent system that recommends the best AI/ML stack
based on user constraints (cost, complexity, scale, goals).
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))))

from unchained import Agent, tool, LLM, RAG, Router
from tools.cost_estimator import estimate_cost
from tools.benchmark_fetcher import fetch_benchmarks
from tools.doc_retriever import retrieve_docs


def build_knowledge_base() -> RAG:
    """Load framework comparison data into RAG."""
    rag = RAG()
    knowledge_dir = os.path.join(os.path.dirname(__file__), "knowledge")

    for filename in os.listdir(knowledge_dir):
        if filename.endswith(".md") or filename.endswith(".txt"):
            filepath = os.path.join(knowledge_dir, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            rag.add(content, metadata={"source": filename})

    return rag


def create_pickmystack_agents(llm: LLM) -> Router:
    """Create the multi-agent evaluation system."""
    rag = build_knowledge_base()

    cost_agent = Agent(
        name="cost_evaluator",
        system_prompt=(
            "You are a cost analysis expert for AI/ML frameworks. "
            "Evaluate the total cost of ownership: API costs, hosting, "
            "infrastructure, and hidden costs. Always provide monthly estimates."
        ),
        llm=llm,
        tools=[estimate_cost],
        rag=rag,
    )

    fit_agent = Agent(
        name="fit_evaluator",
        system_prompt=(
            "You are a framework fit analyst. Score how well each framework "
            "matches the user's specific requirements: team size, use case, "
            "complexity tolerance, and scale needs. Score 0-100."
        ),
        llm=llm,
        tools=[retrieve_docs, fetch_benchmarks],
        rag=rag,
    )

    trend_agent = Agent(
        name="trend_evaluator",
        system_prompt=(
            "You are a technology trends analyst. Evaluate framework health: "
            "GitHub stars, commit frequency, community size, corporate backing, "
            "and momentum. Flag risks like abandonment or major API changes."
        ),
        llm=llm,
        tools=[fetch_benchmarks],
        rag=rag,
    )

    synthesizer = Agent(
        name="synthesizer",
        system_prompt=(
            "You are a senior AI architect. Given evaluations from cost, fit, "
            "and trend analysts, synthesize a final ranked recommendation. "
            "Present top 3 options with clear reasoning. Format as a comparison table."
        ),
        llm=llm,
        rag=rag,
    )

    return Router(
        agents=[cost_agent, fit_agent, trend_agent, synthesizer],
        llm=llm,
    )


def run_pickmystack(user_query: str, provider: str = "ollama",
                    model: str = "llama3.2", api_key: str = None) -> str:
    """Run the full PickMyStack evaluation pipeline."""
    llm = LLM(provider=provider, model=model, api_key=api_key)
    router = create_pickmystack_agents(llm)

    # Run ALL agents and synthesize (not just route to one)
    results = router.run_all(user_query)

    # Final synthesis pass
    synthesis_prompt = (
        f"User request: {user_query}\n\n"
        f"Cost Analysis:\n{results.get('cost_evaluator', 'N/A')}\n\n"
        f"Fit Analysis:\n{results.get('fit_evaluator', 'N/A')}\n\n"
        f"Trend Analysis:\n{results.get('trend_evaluator', 'N/A')}\n\n"
        "Synthesize these into a final ranked recommendation (top 3 stacks)."
    )

    synthesizer = router.agents["synthesizer"]
    return synthesizer.run(synthesis_prompt)


if __name__ == "__main__":
    print("=" * 60)
    print("  PickMyStack.ai — AI Framework Advisor")
    print("  Powered by Unchained")
    print("=" * 60)
    print()

    query = input("Describe your use case (e.g., 'Build a customer support "
                  "chatbot, budget $50/month, solo developer'):\n> ")

    print("\nAnalyzing with multi-agent evaluation pipeline...\n")
    result = run_pickmystack(query)
    print(result)
