# Deploying PickMyStack.ai

## Option 1: Streamlit Community Cloud (Easiest, Free)

1. Push the entire `unchained` repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. Set main file: `examples/pickmystack/ui/app_ui.py`
5. Deploy! 🚀

Your app will be live at: `https://your-app-name.streamlit.app`

## Option 2: HuggingFace Spaces (Free, ML Community)

1. Create a new Space at [huggingface.co/spaces](https://huggingface.co/spaces)
2. Select SDK: **Streamlit**
3. Upload files:
   - `unchained.py` (the framework)
   - `examples/pickmystack/` (the app)
   - `requirements.txt`
4. Set app file: `ui/app_ui.py`

## Option 3: Local Development

```bash
# From project root
pip install -e ".[ui]"
streamlit run examples/pickmystack/ui/app_ui.py
```

Opens at: http://localhost:8501

## Option 4: Docker

```bash
cd examples/pickmystack/ui
docker build -t pickmystack .
docker run -p 8501:8501 pickmystack
```

## Environment Variables (for cloud LLMs)

```bash
# Only needed if using cloud providers (Ollama works without keys)
export OPENAI_API_KEY=sk-...
export ANTHROPIC_API_KEY=sk-ant-...
```

## Notes

- **Ollama mode requires a local machine** — won't work on Streamlit Cloud/HF Spaces
- For cloud deployment, use OpenAI or Anthropic provider
- For local demos (portfolio showcase), Ollama is perfect and free
- The app gracefully handles missing LLM connections with helpful error messages
