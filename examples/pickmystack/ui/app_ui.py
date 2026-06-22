"""
PickMyStack.ai — Streamlit Frontend
The live demo that showcases Unchained's multi-agent capabilities.

Run: streamlit run examples/pickmystack/ui/app_ui.py
"""
import streamlit as st
import sys
import os
import time

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))))

from unchained import Agent, tool, LLM, RAG, Router

# ── Page Config ──────────────────────────────────────────────

st.set_page_config(
    page_title="PickMyStack.ai — AI Framework Advisor",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ───────────────────────────────────────────────

st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1rem 0;
    }
    .main-header h1 {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: 800;
    }
    .subtitle {
        text-align: center;
        color: #6b7280;
        font-size: 1.2rem;
        margin-top: -1rem;
    }
    .powered-by {
        text-align: center;
        color: #9ca3af;
        font-size: 0.85rem;
        margin-bottom: 2rem;
    }
    .recommendation-card {
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
        border: 1px solid #bae6fd;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    .recommendation-card h3 {
        color: #0369a1;
        margin-top: 0;
    }
    .metric-card {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 1rem;
        text-align: center;
    }
    .agent-badge {
        display: inline-block;
        background: #ede9fe;
        color: #6d28d9;
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 0.75rem;
        margin: 2px;
    }
    .stAlert {
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# ── Header ───────────────────────────────────────────────────

st.markdown("""
<div class="main-header">
    <h1>🎯 PickMyStack.ai</h1>
</div>
<p class="subtitle">Stop guessing. Get data-driven AI stack recommendations.</p>
<p class="powered-by">Powered by <b>Unchained</b> — a complete agent framework in 418 lines</p>
""", unsafe_allow_html=True)

# ── Sidebar: Configuration ───────────────────────────────────

with st.sidebar:
    st.header("⚙️ Configuration")

    provider = st.selectbox(
        "LLM Provider",
        ["ollama (Free, Local)", "openai", "anthropic"],
        help="Ollama is free and runs locally. Others need API keys."
    )

    if "ollama" in provider:
        provider_key = "ollama"
        model = st.selectbox("Model", ["llama3.2", "llama3.1", "mistral",
                                        "qwen2.5", "phi3", "gemma2"])
        api_key = None
    elif provider == "openai":
        provider_key = "openai"
        model = st.selectbox("Model", ["gpt-4o-mini", "gpt-4o"])
        api_key = st.text_input("API Key", type="password")
    else:
        provider_key = "anthropic"
        model = st.selectbox("Model", ["claude-3-5-haiku-20241022",
                                        "claude-3-5-sonnet-20241022"])
        api_key = st.text_input("API Key", type="password")

    st.divider()
    st.header("📊 How It Works")
    st.markdown("""
    **4 specialized agents** evaluate your requirements:

    1. 💰 **CostAgent** — Estimates monthly costs
    2. 🎯 **FitAgent** — Scores framework match
    3. 📈 **TrendAgent** — Checks community health
    4. 🧠 **Synthesizer** — Produces final ranking
    """)

    st.divider()
    st.caption("Built with Unchained (418 lines)")
    st.caption("[GitHub](https://github.com/YOUR_USERNAME/unchained) • MIT License")

# ── Knowledge Base ───────────────────────────────────────────

@st.cache_resource
def load_knowledge_base():
    """Load framework knowledge into RAG."""
    rag = RAG()
    knowledge_dir = os.path.join(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__))), "knowledge")

    if os.path.exists(knowledge_dir):
        for filename in os.listdir(knowledge_dir):
            if filename.endswith((".md", ".txt")):
                filepath = os.path.join(knowledge_dir, filename)
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                rag.add(content, metadata={"source": filename})
    return rag


# ── Framework Data (for quick display) ───────────────────────

FRAMEWORKS = {
    "LangChain": {"stars": "95k+", "learning": "High", "best": "Complex pipelines, enterprise"},
    "LlamaIndex": {"stars": "37k+", "learning": "Medium", "best": "Document Q&A, RAG"},
    "CrewAI": {"stars": "22k+", "learning": "Low-Med", "best": "Multi-agent workflows"},
    "AutoGen": {"stars": "35k+", "learning": "High", "best": "Code gen, agent collaboration"},
    "DSPy": {"stars": "18k+", "learning": "High", "best": "Prompt optimization, research"},
    "Unchained": {"stars": "New", "learning": "Very Low", "best": "Simplicity, prototyping, $0 cost"},
}

# ── Main Input ───────────────────────────────────────────────

st.markdown("---")

col1, col2 = st.columns([2, 1])

with col1:
    use_case = st.text_area(
        "🎯 Describe what you want to build",
        placeholder="e.g., 'Build a customer support chatbot that answers questions from our documentation. Budget: $0 for prototyping. Team: just me. Scale: ~100 users initially.'",
        height=120,
    )

with col2:
    st.markdown("**Quick constraints:**")
    budget = st.select_slider(
        "💰 Monthly budget",
        options=["$0", "$10", "$25", "$50", "$100", "$200+"],
        value="$0"
    )
    team_size = st.radio(
        "👥 Team size",
        ["Solo developer", "Small team (2-5)", "Large team (5+)"],
        horizontal=True
    )
    priority = st.multiselect(
        "⭐ Top priorities",
        ["Low cost", "Simplicity", "Production-ready", "Scalability",
         "Community support", "Privacy/local"],
        default=["Low cost", "Simplicity"]
    )

# ── Analysis ─────────────────────────────────────────────────

analyze_btn = st.button("🚀 Analyze & Recommend", type="primary",
                        use_container_width=True, disabled=not use_case)

if analyze_btn and use_case:
    # Build full query
    full_query = (
        f"Use case: {use_case}\n"
        f"Budget: {budget}/month\n"
        f"Team: {team_size}\n"
        f"Priorities: {', '.join(priority)}"
    )

    # Progress display
    progress = st.progress(0, text="Initializing agents...")

    try:
        llm = LLM(provider=provider_key, model=model, api_key=api_key)
        rag = load_knowledge_base()

        # Agent 1: Cost Analysis
        progress.progress(15, text="💰 CostAgent analyzing pricing...")

        cost_agent = Agent(
            name="cost_evaluator",
            system_prompt=(
                "You are a cost analysis expert for AI/ML frameworks. "
                "Evaluate total cost of ownership: API costs, hosting, infrastructure. "
                "Provide monthly estimates. Be specific with dollar amounts."
            ),
            llm=llm, rag=rag,
        )
        cost_result = cost_agent.run(full_query)
        progress.progress(35, text="🎯 FitAgent scoring framework match...")

        # Agent 2: Fit Analysis
        fit_agent = Agent(
            name="fit_evaluator",
            system_prompt=(
                "You are a framework fit analyst. Score how well each framework "
                "matches the user's requirements: team size, use case, complexity "
                "tolerance, and scale. Score each framework 0-100. Be decisive."
            ),
            llm=llm, rag=rag,
        )
        fit_result = fit_agent.run(full_query)
        progress.progress(60, text="📈 TrendAgent checking community health...")

        # Agent 3: Trend Analysis
        trend_agent = Agent(
            name="trend_evaluator",
            system_prompt=(
                "You are a technology trends analyst. Evaluate framework health: "
                "GitHub stars, commit frequency, community size, momentum. "
                "Flag risks like abandonment or breaking changes."
            ),
            llm=llm, rag=rag,
        )
        trend_result = trend_agent.run(full_query)
        progress.progress(80, text="🧠 Synthesizer ranking recommendations...")

        # Agent 4: Synthesizer
        synthesizer = Agent(
            name="synthesizer",
            system_prompt=(
                "You are a senior AI architect. Given cost, fit, and trend analyses, "
                "produce a FINAL ranked recommendation (top 3 stacks). "
                "For each: name the stack components, monthly cost estimate, "
                "fit score (0-100), and one-line reasoning. Format clearly."
            ),
            llm=llm, rag=rag,
        )

        synthesis_query = (
            f"User request: {full_query}\n\n"
            f"--- Cost Analysis ---\n{cost_result}\n\n"
            f"--- Fit Analysis ---\n{fit_result}\n\n"
            f"--- Trend Analysis ---\n{trend_result}\n\n"
            "Synthesize into a final TOP 3 ranked recommendation."
        )
        final_result = synthesizer.run(synthesis_query)
        progress.progress(100, text="✅ Analysis complete!")
        time.sleep(0.5)
        progress.empty()

        # ── Display Results ──────────────────────────────────
        st.markdown("---")
        st.header("🏆 Recommendation")
        st.markdown(final_result)

        # Expandable details
        with st.expander("💰 Full Cost Analysis"):
            st.markdown(cost_result)

        with st.expander("🎯 Full Fit Analysis"):
            st.markdown(fit_result)

        with st.expander("📈 Full Trend Analysis"):
            st.markdown(trend_result)

        # Token usage
        total_tokens = (cost_agent.token_usage + fit_agent.token_usage +
                       trend_agent.token_usage + synthesizer.token_usage)
        st.caption(f"📊 Total tokens used: {total_tokens:,} | "
                  f"Provider: {provider_key} | Model: {model}")

    except Exception as e:
        progress.empty()
        st.error(f"⚠️ Error: {str(e)}")
        if "ollama" in provider:
            st.info("💡 Make sure Ollama is running: `ollama serve` and you've "
                   "pulled the model: `ollama pull llama3.2`")
        else:
            st.info("💡 Check your API key and try again.")

# ── Quick Comparison Table (always visible) ──────────────────

st.markdown("---")
st.header("📋 Framework Quick Reference")

cols = st.columns(len(FRAMEWORKS))
for i, (name, data) in enumerate(FRAMEWORKS.items()):
    with cols[i]:
        st.markdown(f"**{name}**")
        st.caption(f"⭐ {data['stars']}")
        st.caption(f"📚 {data['learning']}")
        st.caption(f"🎯 {data['best']}")

# ── Footer ───────────────────────────────────────────────────

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #9ca3af; padding: 1rem;">
    <p><b>PickMyStack.ai</b> — Built entirely on <a href="https://github.com/YOUR_USERNAME/unchained">Unchained</a> (418 lines, 2 dependencies)</p>
    <p>Proving that a minimal framework can power real multi-agent applications.</p>
</div>
""", unsafe_allow_html=True)
