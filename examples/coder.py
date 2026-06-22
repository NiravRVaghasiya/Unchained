"""
Example: Code Assistant Agent — 25 lines.
Executes Python code safely and explains results.
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from unchained import Agent, tool, LLM


@tool
def run_code(code: str) -> str:
    """Execute Python code and return the output. Only safe operations allowed."""
    try:
        # Restricted execution environment
        allowed_builtins = {"print": print, "len": len, "range": range,
                           "int": int, "float": float, "str": str,
                           "list": list, "dict": dict, "sum": sum,
                           "min": min, "max": max, "sorted": sorted,
                           "enumerate": enumerate, "zip": zip, "map": map}
        import io, contextlib
        output = {}
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            exec(code, {"__builtins__": allowed_builtins}, output)
        printed = buf.getvalue()
        if printed:
            return printed
        return str(output) if output else "Code executed successfully (no output)."
    except Exception as e:
        return f"Error: {e}"


agent = Agent(
    name="coder",
    system_prompt="You are a Python coding assistant. Write and execute code to solve problems. Explain your approach.",
    llm=LLM(provider="ollama", model="llama3.2"),
    tools=[run_code],
    verbose=True,
)

if __name__ == "__main__":
    query = input("Coding task: ") if len(sys.argv) < 2 else " ".join(sys.argv[1:])
    print(agent.run(query))
