"""
Cost Estimator Tool — Estimates monthly costs for AI/ML stacks.
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))))

from unchained import tool

# Pricing data (updated periodically)
PRICING = {
    "models": {
        "gpt-4o": {"input": 2.50, "output": 10.00, "per": "1M tokens"},
        "gpt-4o-mini": {"input": 0.15, "output": 0.60, "per": "1M tokens"},
        "claude-3.5-sonnet": {"input": 3.00, "output": 15.00, "per": "1M tokens"},
        "claude-3.5-haiku": {"input": 0.80, "output": 4.00, "per": "1M tokens"},
        "llama3.2-local": {"input": 0, "output": 0, "per": "free (local GPU)"},
        "mistral-7b-local": {"input": 0, "output": 0, "per": "free (local GPU)"},
        "gemini-1.5-flash": {"input": 0.075, "output": 0.30, "per": "1M tokens"},
    },
    "vector_dbs": {
        "pinecone": {"free_tier": True, "paid": "$70/month (s1.x1 pod)"},
        "weaviate_cloud": {"free_tier": True, "paid": "$25/month (starter)"},
        "chromadb": {"free_tier": True, "paid": "$0 (self-hosted)"},
        "qdrant": {"free_tier": True, "paid": "$0 (self-hosted) / $25 cloud"},
        "faiss": {"free_tier": True, "paid": "$0 (in-memory, self-hosted)"},
    },
    "frameworks": {
        "langchain": {"cost": "$0", "hidden": "complexity tax, debugging time"},
        "llamaindex": {"cost": "$0", "hidden": "opinionated, lock-in risk"},
        "crewai": {"cost": "$0 OSS / $200 enterprise", "hidden": "still maturing"},
        "autogen": {"cost": "$0", "hidden": "Microsoft ecosystem coupling"},
        "unchained": {"cost": "$0", "hidden": "minimal ecosystem (but that's the point)"},
    },
    "hosting": {
        "huggingface_spaces": {"free": True, "paid": "$9/month (GPU)"},
        "streamlit_cloud": {"free": True, "paid": "$0 (community tier)"},
        "railway": {"free": False, "paid": "$5/month + usage"},
        "aws_lambda": {"free_tier": True, "paid": "~$3-20/month"},
        "local_ollama": {"free": True, "paid": "$0 (your hardware)"},
    },
}


@tool
def estimate_cost(use_case: str, budget: str, scale: str) -> str:
    """Estimate monthly costs for different AI stack options.

    Args:
        use_case: What the user wants to build
        budget: User's budget constraint (e.g., '$0', '$50/month', 'unlimited')
        scale: Expected scale (e.g., '100 users', '10k requests/day')
    """
    # Parse budget
    budget_val = 0
    if "$" in budget:
        import re
        nums = re.findall(r'\d+', budget)
        budget_val = int(nums[0]) if nums else 0

    report = f"## Cost Analysis for: {use_case}\n"
    report += f"Budget: {budget} | Scale: {scale}\n\n"

    # Recommend tiers
    if budget_val == 0:
        report += "### Zero-Cost Stack:\n"
        report += "- Model: Llama 3.2 via Ollama (free, local)\n"
        report += "- Vector DB: ChromaDB or FAISS (free, in-memory)\n"
        report += "- Framework: Unchained (zero dependencies)\n"
        report += "- Hosting: Streamlit Community Cloud / HuggingFace Spaces\n"
        report += "- **Total: $0/month**\n\n"

    if budget_val <= 50:
        report += "### Budget Stack ($15-30/month):\n"
        report += "- Model: GPT-4o-mini ($0.15/1M input tokens)\n"
        report += "- Vector DB: Qdrant Cloud Free Tier\n"
        report += "- Framework: LlamaIndex or Unchained\n"
        report += "- Hosting: Railway ($5/month)\n"
        report += "- **Estimated: $15-30/month at moderate scale**\n\n"

    if budget_val >= 50:
        report += "### Production Stack ($50-150/month):\n"
        report += "- Model: GPT-4o or Claude 3.5 Sonnet\n"
        report += "- Vector DB: Pinecone ($70/month) or Weaviate\n"
        report += "- Framework: LangChain (full ecosystem)\n"
        report += "- Hosting: AWS Lambda + API Gateway\n"
        report += "- **Estimated: $80-150/month**\n"

    report += f"\n### Pricing Data:\n"
    report += "Models: " + ", ".join(
        f"{k}: ${v['input']}/{v['output']} per 1M tokens"
        for k, v in PRICING["models"].items() if v["input"] > 0
    )

    return report
