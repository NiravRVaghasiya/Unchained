# Deployment Options for AI Applications

## Free Tier Options

### Streamlit Community Cloud
- Cost: $0
- Limits: 1GB RAM, shared resources
- Best for: Demos, MVPs, portfolio projects
- Setup: Connect GitHub repo, deploy in 2 clicks
- URL: your-app.streamlit.app

### HuggingFace Spaces
- Cost: $0 (CPU) / $9/month (GPU)
- Limits: 2 vCPU, 16GB RAM (free tier)
- Best for: ML demos, Gradio apps, model showcases
- Setup: Push to HF repo, auto-deploys
- Bonus: Built-in community + discoverability

### Vercel (for frontends)
- Cost: $0 (hobby)
- Best for: Next.js/React frontends that call your API
- Limits: Serverless functions, 10s timeout

### Railway
- Cost: $5/month + usage (500 free hours)
- Best for: Always-on backends, APIs
- Setup: Connect GitHub, auto-deploy

## Budget Options ($10-50/month)

### AWS Lambda + API Gateway
- Cost: ~$3-20/month for moderate traffic
- Best for: Serverless AI APIs, pay-per-request
- Pros: Scales to zero, no idle costs
- Cons: Cold starts, 15-min timeout

### Google Cloud Run
- Cost: ~$5-30/month
- Best for: Containerized apps, auto-scaling
- Pros: Scale to zero, generous free tier
- Cons: Cold starts for infrequent traffic

### Render
- Cost: $7/month (starter)
- Best for: Simple web services
- Pros: Easy deployment, free TLS
- Cons: Limited compute

## Running Local LLMs (Zero Cost)

### Ollama
- Install: curl -fsSL https://ollama.com/install.sh | sh
- Pull model: ollama pull llama3.2
- Use in Unchained: LLM(provider="ollama", model="llama3.2")
- Requirements: 8GB RAM minimum
- Supported: Llama 3.2, Mistral, Phi-3, Qwen, Gemma

### LM Studio
- GUI-based local model runner
- Download any GGUF model
- OpenAI-compatible API on localhost
- Good for: Non-technical users who want local AI

## Decision Tree

1. Portfolio demo? → Streamlit Cloud or HuggingFace Spaces (free)
2. Need GPU for inference? → HuggingFace Spaces ($9/month)
3. Production API? → Railway ($5) or Cloud Run
4. Enterprise scale? → AWS ECS/EKS or GCP GKE
5. Zero cost everything? → Ollama locally + Streamlit Cloud for demo
