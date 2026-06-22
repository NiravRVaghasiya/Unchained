# LLM Model Selection Guide

## Cloud Models (Pay-per-token)

### GPT-4o (OpenAI)
- Best for: Complex reasoning, code generation, multi-modal
- Cost: $2.50/1M input, $10/1M output
- Context: 128K tokens
- Speed: Fast
- When to use: Budget available, need top quality

### GPT-4o-mini (OpenAI)
- Best for: Most tasks where GPT-4o is overkill
- Cost: $0.15/1M input, $0.60/1M output (93% cheaper than GPT-4o)
- Context: 128K tokens
- Speed: Very fast
- When to use: Default choice for most applications

### Claude 3.5 Sonnet (Anthropic)
- Best for: Long documents, nuanced writing, analysis
- Cost: $3/1M input, $15/1M output
- Context: 200K tokens
- Speed: Fast
- When to use: Long-context tasks, careful analysis

### Claude 3.5 Haiku (Anthropic)
- Best for: Fast, cheap tasks with good quality
- Cost: $0.80/1M input, $4/1M output
- Context: 200K tokens
- Speed: Very fast
- When to use: High-volume, cost-sensitive applications

### Gemini 1.5 Flash (Google)
- Best for: Multi-modal, long context, budget-friendly
- Cost: $0.075/1M input, $0.30/1M output (cheapest major model)
- Context: 1M tokens
- Speed: Fast
- When to use: Extremely long documents, video/audio processing

## Local Models (Free via Ollama)

### Llama 3.2 (Meta)
- Best for: General purpose, tool calling
- Cost: $0 (runs on your hardware)
- Requirements: 8GB RAM minimum (3B), 16GB for 8B
- When to use: Zero-budget projects, privacy requirements

### Mistral 7B
- Best for: Fast inference, European compliance
- Cost: $0 (local)
- Requirements: 8GB RAM
- When to use: Speed-critical, GDPR-sensitive

### Qwen 2.5 (Alibaba)
- Best for: Multilingual, coding
- Cost: $0 (local)
- Requirements: 8GB RAM (7B version)
- When to use: Non-English applications, code generation

### Phi-3 (Microsoft)
- Best for: Small/embedded devices, reasoning
- Cost: $0 (local)
- Requirements: 4GB RAM (mini version)
- When to use: Edge deployment, resource-constrained

## Model Selection Decision Tree

1. Budget = $0? → Ollama + Llama 3.2
2. Need 200K+ context? → Claude 3.5 Sonnet or Gemini Flash
3. Need cheapest cloud? → Gemini 1.5 Flash ($0.075/1M input)
4. Need best quality? → GPT-4o or Claude 3.5 Sonnet
5. High volume, good-enough quality? → GPT-4o-mini
6. Privacy/on-premise required? → Ollama + any local model
