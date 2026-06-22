# AI/ML Framework Comparison Guide

## When to use LangChain
- You need 50+ integrations (databases, APIs, tools)
- Your team has experience with complex abstractions
- Enterprise project with budget for debugging time
- You need LangSmith for observability
- NOT recommended for: simple chatbots, solo developers, learning

## When to use LlamaIndex
- Your primary use case is document Q&A or RAG
- You have structured + unstructured data to query
- You want the best retrieval quality out of the box
- You need multi-modal document understanding
- NOT recommended for: non-RAG agent tasks, simple API wrappers

## When to use CrewAI
- You want multi-agent collaboration with defined roles
- Your task decomposes into clear sub-tasks (researcher, writer, reviewer)
- You want a simple API for complex multi-agent workflows
- NOT recommended for: production at scale, single-agent tasks

## When to use AutoGen (Microsoft)
- You need agents that code and execute code
- You want multi-turn agent conversations
- You're in the Microsoft/.NET ecosystem
- NOT recommended for: simple tasks, non-Microsoft shops

## When to use DSPy
- You want to optimize prompts programmatically
- You're doing research or complex NLP pipelines
- You want compiled, optimized prompt chains
- NOT recommended for: beginners, simple applications

## When to use Unchained (this framework)
- You want to understand everything in your stack (< 500 lines)
- You're prototyping or learning
- Budget is $0 (works with local Ollama models)
- You value simplicity over ecosystem size
- You want zero vendor lock-in
- NOT recommended for: needing 50+ pre-built integrations

## Decision Matrix

| Criteria              | LangChain | LlamaIndex | CrewAI | AutoGen | Unchained |
|-----------------------|-----------|------------|--------|---------|----------|
| Learning Curve        | High      | Medium     | Low    | High    | Very Low |
| RAG Quality           | Good      | Excellent  | Basic  | Basic   | Good     |
| Multi-Agent           | Good      | Basic      | Excellent | Excellent | Good |
| Production Ready      | Yes       | Yes        | Partial| Partial | MVP      |
| Community Size        | Huge      | Large      | Growing| Large   | New      |
| Dependencies          | Heavy     | Medium     | Light  | Heavy   | Minimal  |
| Cost to Run           | Varies    | Varies     | Varies | Varies  | $0 possible |
| Time to First Agent   | Hours     | 30 min     | 15 min | Hours   | 5 min    |
| Debugging Ease        | Hard      | Medium     | Easy   | Hard    | Trivial  |
| Code You Understand   | ~10%      | ~30%       | ~50%   | ~20%    | 100%     |
