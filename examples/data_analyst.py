"""
Example: Data Analyst Agent — 20 lines.
Analyzes CSV data and provides insights.
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from unchained import Agent, tool, LLM


@tool
def analyze_csv(file_path: str) -> str:
    """Read and summarize a CSV file. Returns column info, shape, and sample rows."""
    import csv
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    if not rows:
        return "Empty CSV file."
    cols = list(rows[0].keys())
    summary = f"Columns ({len(cols)}): {', '.join(cols)}\n"
    summary += f"Rows: {len(rows)}\n"
    summary += f"Sample (first 3):\n"
    for row in rows[:3]:
        summary += f"  {dict(row)}\n"
    return summary


agent = Agent(
    name="analyst",
    system_prompt="You are a data analyst. Analyze datasets and provide clear, actionable insights with statistics.",
    llm=LLM(provider="ollama", model="llama3.2"),
    tools=[analyze_csv],
    verbose=True,
)

if __name__ == "__main__":
    query = input("Analysis task: ") if len(sys.argv) < 2 else " ".join(sys.argv[1:])
    print(agent.run(query))
