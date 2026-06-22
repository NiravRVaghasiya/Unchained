"""
Benchmark Fetcher Tool — Fetches framework comparison data.
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))))

from unchained import tool

# Framework benchmark data (curated from public sources)
BENCHMARKS = {
    "langchain": {
        "github_stars": "95k+",
        "weekly_downloads": "2M+",
        "first_release": "Oct 2022",
        "latest_version": "0.3.x",
        "languages": ["Python", "JavaScript"],
        "strengths": ["Huge ecosystem", "Many integrations", "Large community"],
        "weaknesses": ["Complexity", "Frequent breaking changes", "Abstraction overhead"],
        "best_for": ["Complex RAG pipelines", "Enterprise apps", "Multi-chain workflows"],
        "learning_curve": "High",
        "production_ready": "Yes (with effort)",
        "lines_for_basic_agent": "~50-100",
    },
    "llamaindex": {
        "github_stars": "37k+",
        "weekly_downloads": "800k+",
        "first_release": "Nov 2022",
        "latest_version": "0.11.x",
        "languages": ["Python", "TypeScript"],
        "strengths": ["Best RAG framework", "Good docs", "Data-focused"],
        "weaknesses": ["Opinionated", "Less flexible for non-RAG tasks"],
        "best_for": ["Document Q&A", "Knowledge bases", "Structured data querying"],
        "learning_curve": "Medium",
        "production_ready": "Yes",
        "lines_for_basic_agent": "~30-60",
    },
    "crewai": {
        "github_stars": "22k+",
        "weekly_downloads": "400k+",
        "first_release": "Dec 2023",
        "latest_version": "0.80.x",
        "languages": ["Python"],
        "strengths": ["Multi-agent focus", "Role-based design", "Simple API"],
        "weaknesses": ["Still maturing", "Limited tool ecosystem", "Less battle-tested"],
        "best_for": ["Multi-agent workflows", "Role-playing agents", "Task automation"],
        "learning_curve": "Low-Medium",
        "production_ready": "Experimental",
        "lines_for_basic_agent": "~20-40",
    },
    "autogen": {
        "github_stars": "35k+",
        "weekly_downloads": "300k+",
        "first_release": "Sep 2023",
        "latest_version": "0.4.x",
        "languages": ["Python", ".NET"],
        "strengths": ["Multi-agent conversations", "Microsoft backing", "Code execution"],
        "weaknesses": ["Complex setup", "Heavy abstraction", "Microsoft-centric"],
        "best_for": ["Agent collaboration", "Code generation", "Research prototyping"],
        "learning_curve": "High",
        "production_ready": "Experimental",
        "lines_for_basic_agent": "~30-50",
    },
    "semantic_kernel": {
        "github_stars": "22k+",
        "weekly_downloads": "100k+",
        "first_release": "Mar 2023",
        "latest_version": "1.x",
        "languages": ["Python", "C#", "Java"],
        "strengths": ["Enterprise-grade", "Multi-language", "Plugin system"],
        "weaknesses": ["Microsoft ecosystem lock-in", "Verbose"],
        "best_for": ["Enterprise AI", ".NET shops", "Plugin architectures"],
        "learning_curve": "Medium-High",
        "production_ready": "Yes",
        "lines_for_basic_agent": "~40-80",
    },
    "dspy": {
        "github_stars": "18k+",
        "weekly_downloads": "200k+",
        "first_release": "2023",
        "latest_version": "2.x",
        "languages": ["Python"],
        "strengths": ["Programmatic prompting", "Optimization", "Research-backed"],
        "weaknesses": ["Steep learning curve", "Academic feel", "Small community"],
        "best_for": ["Prompt optimization", "Research", "Complex NLP pipelines"],
        "learning_curve": "High",
        "production_ready": "Experimental",
        "lines_for_basic_agent": "~20-30",
    },
    "unchained": {
        "github_stars": "new",
        "weekly_downloads": "new",
        "first_release": "2025",
        "latest_version": "0.1.0",
        "languages": ["Python"],
        "strengths": ["Minimal (<500 lines)", "Zero bloat", "Easy to understand",
                      "No vendor lock-in", "Free with Ollama"],
        "weaknesses": ["Small ecosystem", "No enterprise support", "New project"],
        "best_for": ["Learning", "Prototyping", "When simplicity matters",
                     "Cost-sensitive projects"],
        "learning_curve": "Very Low",
        "production_ready": "MVP",
        "lines_for_basic_agent": "~5-10",
    },
}


@tool
def fetch_benchmarks(framework_name: str) -> str:
    """Fetch benchmark and comparison data for a specific framework.

    Args:
        framework_name: Name of the framework (e.g., 'langchain', 'crewai')
    """
    name = framework_name.lower().replace(" ", "_").replace("-", "_")

    if name in BENCHMARKS:
        data = BENCHMARKS[name]
        report = f"## {framework_name} Benchmarks\n\n"
        for key, value in data.items():
            label = key.replace("_", " ").title()
            if isinstance(value, list):
                report += f"- **{label}**: {', '.join(value)}\n"
            else:
                report += f"- **{label}**: {value}\n"
        return report

    # Return all frameworks for comparison
    report = f"Framework '{framework_name}' not found. Available frameworks:\n\n"
    for fw_name, data in BENCHMARKS.items():
        report += (f"- **{fw_name}**: {data['github_stars']} stars, "
                   f"Best for: {', '.join(data['best_for'][:2])}\n")
    return report
