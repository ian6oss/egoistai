---
title: "Best Local LLMs in 2026: Run AI Without the Cloud"
excerpt: "The best open-source LLMs you can run on your own hardware right now — no API keys, no subscriptions, no data leaving your machine."
category: "Tools"
categorySlug: "tools"
image: "/images/best-local-llms-2026.webp"
date: "2026-03-26"
readTime: "11 min read"
author: "EgoistAI"
featured: false
tags: ["ai", "local-llm", "ollama", "llama", "privacy", "open-source", "self-hosted"]
sources:
  - name: "Meta AI - Llama Model Collection"
    url: "https://ai.meta.com/llama/"
  - name: "Ollama - Official Documentation"
    url: "https://ollama.com/"
  - name: "Hugging Face Open LLM Leaderboard"
    url: "https://huggingface.co/spaces/open-llm-leaderboard/open_llm_leaderboard"
---

Let's cut straight to it: you don't need OpenAI. You don't need Anthropic. You don't need Google. Not for everything, anyway.

In 2026, local LLMs have crossed the threshold from "interesting toy for hobbyists" to "genuinely useful tools that compete with cloud APIs for a huge range of tasks." The models are better. The tooling is smoother. And the hardware requirements have dropped enough that a decent laptop can run a capable model without melting.

This isn't another spec-sheet listicle. This is an implementation guide. By the end, you'll have models running on your machine, integrated into your apps, and serving inference through Docker containers. We're covering installation, code, hardware, benchmarks, and real decision-making frameworks.

Let's get your hands dirty.

## Why Run LLMs Locally?

**Privacy is the obvious one.** When you send a prompt to a cloud API, your data hits someone else's servers. If you're working with proprietary code, medical records, legal documents, or anything you genuinely can't afford to leak — local inference is the only real answer. Your data never leaves your machine. Period.

**Cost is the second reason.** Cloud API pricing adds up fast. A local model has zero marginal cost per inference. You pay for the hardware once, and every query after that is free. If you're running RAG pipelines, batch processing, or agent loops, the savings compound aggressively.

**Latency matters too.** No network round-trip. No queue. No rate limits. For real-time coding assistants, local search, and interactive tools — local inference wins on speed.

**And then there's reliability.** No outages. No API changes. No sudden deprecation of the model you built your product on. Your local setup works until you decide to change it.

## Hardware Requirements: Know Before You Install

Before downloading anything, let's make sure your machine can handle it. Here's the real-world hardware matrix — not marketing numbers, actual requirements for usable inference speeds.

### Hardware Requirements by Model Size

| Model Size | Min VRAM (GPU) | Min RAM (CPU-only) | Recommended GPU | Storage per Model | Expected Speed |
|-----------|---------------|--------------------|-----------------|--------------------|----------------|
| 1-3B (Phi-4 Mini, Llama 3.2 3B) | 2 GB | 4 GB | Any modern GPU | 1.5 - 2.5 GB | 40-80 tok/s |
| 7-8B (Llama 4 Scout 8B, Mistral 7B, Qwen 2.5 7B) | 6 GB | 8 GB | RTX 4060 / M2 | 4 - 6 GB | 25-50 tok/s |
| 13-14B (Phi-4, Qwen 2.5 14B) | 10 GB | 16 GB | RTX 4070 Ti / M2 Pro | 8 - 10 GB | 15-35 tok/s |
| 30-34B (DeepSeek-R1 32B, Qwen 2.5 32B) | 20 GB | 32 GB | RTX 4090 / M3 Pro | 18 - 22 GB | 10-20 tok/s |
| 70B (Llama 3.1 70B, Qwen 2.5 72B) | 40 GB+ | 64 GB | RTX A6000 / M3 Max | 35 - 45 GB | 5-12 tok/s |
| 100B+ (Llama 4 Scout 109B, DeepSeek-V3) | 80 GB+ | 128 GB | Multi-GPU / M4 Ultra | 60 - 120 GB | 3-8 tok/s |

*All sizes assume Q4_K_M quantization (the sweet spot of quality vs. size). Full-precision models require roughly 2x the VRAM.*

### Performance Benchmarks: Tokens/Second on Real Hardware

| Hardware | Llama 4 Scout 8B (Q4) | Qwen 2.5 14B (Q4) | DeepSeek-R1 32B (Q4) | Llama 3.1 70B (Q4) |
|---------|----------------------|-------------------|---------------------|-------------------|
| M2 MacBook Air (8GB) | 18 tok/s | 6 tok/s | N/A | N/A |
| M3 Pro MacBook Pro (18GB) | 42 tok/s | 28 tok/s | 12 tok/s | N/A |
| M4 Max Mac (64GB) | 58 tok/s | 45 tok/s | 28 tok/s | 14 tok/s |
| RTX 4060 (8GB VRAM) | 45 tok/s | 11 tok/s* | N/A | N/A |
| RTX 4070 Ti (12GB VRAM) | 52 tok/s | 35 tok/s | 8 tok/s* | N/A |
| RTX 4090 (24GB VRAM) | 65 tok/s | 48 tok/s | 25 tok/s | 10 tok/s* |
| RTX A6000 (48GB VRAM) | 70 tok/s | 55 tok/s | 32 tok/s | 18 tok/s |

*\* Requires partial CPU offloading, which significantly reduces speed.*

The Apple Silicon advantage is real. Unified memory means a Mac with 64GB RAM can run a 70B model entirely in memory without the CPU-GPU transfer bottleneck that kills performance on split configurations. If you're buying hardware specifically for local LLMs, Apple Silicon offers the best large-model experience per dollar at the consumer level.

## Step-by-Step Installation: Three Ways to Run Local LLMs

### Method 1: Ollama (Recommended for Most People)

Ollama is the Docker of local LLMs — it just works. Install it, pull a model, and you're generating text in under a minute.

**Install on macOS:**

```bash
# Download and install via Homebrew
brew install ollama

# Or use the official installer
curl -fsSL https://ollama.com/install.sh | sh
```

**Install on Linux:**

```bash
curl -fsSL https://ollama.com/install.sh | sh

# Verify installation
ollama --version
```

**Install on Windows:**

Download the installer from [ollama.com/download](https://ollama.com/download) and run it. Ollama runs as a background service.

**Download and run your first model:**

```bash
# Start the Ollama service (macOS/Linux — starts automatically on Windows)
ollama serve &

# Pull a model (downloads once, cached locally)
ollama pull llama4-scout        # Meta's latest, 8B active params
ollama pull qwen2.5:14b         # Alibaba's powerhouse
ollama pull deepseek-r1:32b     # Reasoning specialist
ollama pull phi4                # Microsoft's efficient 14B
ollama pull mistral             # Mistral 7B, the efficiency king

# Run interactively
ollama run llama4-scout

# Single-shot query
ollama run llama4-scout "Write a Python function that finds all prime numbers up to n using the Sieve of Eratosthenes"

# List downloaded models
ollama list

# Show model details
ollama show llama4-scout
```

**Use Ollama's API (OpenAI-compatible):**

```bash
# Chat completions endpoint — drop-in replacement for OpenAI
curl http://localhost:11434/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama4-scout",
    "messages": [{"role": "user", "content": "Explain quantum computing in one paragraph"}],
    "temperature": 0.7
  }'

# Generate endpoint (Ollama-native)
curl http://localhost:11434/api/generate \
  -d '{
    "model": "llama4-scout",
    "prompt": "What is the capital of France?",
    "stream": false
  }'
```

**Customize model behavior with a Modelfile:**

```dockerfile
# Save as Modelfile
FROM llama4-scout

# Set system prompt
SYSTEM """You are a senior software engineer. You write clean, well-documented code. 
You always explain your reasoning before writing code. You prefer simplicity over cleverness."""

# Adjust parameters
PARAMETER temperature 0.3
PARAMETER top_p 0.9
PARAMETER num_ctx 8192
```

```bash
# Create your custom model
ollama create code-assistant -f Modelfile

# Run it
ollama run code-assistant "Refactor this function to use async/await"
```

### Method 2: LM Studio (Best GUI Experience)

LM Studio is for people who want a polished desktop app. Download it from [lmstudio.ai](https://lmstudio.ai), and you get a model browser, chat interface, and local API server with zero terminal usage.

**Setup steps:**

1. Download LM Studio from the official site (macOS, Windows, Linux beta)
2. Launch the app and browse the model catalog
3. Search for a model (e.g., "llama 4 scout" or "qwen 2.5")
4. Click Download — LM Studio handles GGUF format selection based on your hardware
5. Go to the Chat tab, select your model, and start talking

**Run the local API server:**

In LM Studio, go to the "Developer" tab and click "Start Server." This launches an OpenAI-compatible API on `localhost:1234`. Every tool that works with OpenAI's API works with LM Studio — just swap the base URL.

```bash
# Test the LM Studio server
curl http://localhost:1234/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "loaded-model",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

### Method 3: llama.cpp (Maximum Control)

llama.cpp is the engine under the hood of both Ollama and LM Studio. Use it directly when you need maximum performance tuning, custom quantization, or batch processing.

**Build from source:**

```bash
# Clone the repository
git clone https://github.com/ggerganov/llama.cpp.git
cd llama.cpp

# Build with GPU support

# For NVIDIA CUDA:
cmake -B build -DGGML_CUDA=ON
cmake --build build --config Release -j$(nproc)

# For Apple Metal (macOS):
cmake -B build -DGGML_METAL=ON
cmake --build build --config Release -j$(sysctl -n hw.ncpu)

# For CPU only:
cmake -B build
cmake --build build --config Release -j$(nproc)
```

**Download a model (GGUF format from Hugging Face):**

```bash
# Install huggingface-cli if you don't have it
pip install huggingface-hub

# Download a quantized model
huggingface-cli download bartowski/Meta-Llama-4-Scout-17B-16E-Instruct-GGUF \
  Meta-Llama-4-Scout-17B-16E-Instruct-Q4_K_M.gguf \
  --local-dir ./models
```

**Run inference:**

```bash
# Interactive chat mode
./build/bin/llama-cli \
  -m ./models/Meta-Llama-4-Scout-17B-16E-Instruct-Q4_K_M.gguf \
  --chat-template llama4 \
  -ngl 99 \        # Offload all layers to GPU
  -c 8192 \        # Context window size
  -t 8 \           # Number of CPU threads
  --interactive

# Start an OpenAI-compatible API server
./build/bin/llama-server \
  -m ./models/Meta-Llama-4-Scout-17B-16E-Instruct-Q4_K_M.gguf \
  --host 0.0.0.0 \
  --port 8080 \
  -ngl 99 \
  -c 8192 \
  --threads 8
```

**Quantize your own models:**

```bash
# Convert a Hugging Face model to GGUF
python convert_hf_to_gguf.py /path/to/model --outfile model-f16.gguf

# Quantize to Q4_K_M (best balance of quality and size)
./build/bin/llama-quantize model-f16.gguf model-q4km.gguf Q4_K_M

# Other quantization options:
# Q2_K   - Smallest, lowest quality (desperate times)
# Q4_K_M - Sweet spot for most use cases
# Q5_K_M - Higher quality, ~25% more VRAM
# Q6_K   - Near-lossless, ~50% more VRAM
# Q8_0   - Basically lossless, nearly full-size
```

## Python Integration: Build Apps with Local LLMs

This is where it gets real. Here's how to wire local LLMs into actual applications.

### Using the OpenAI SDK (Works with Ollama, LM Studio, llama.cpp)

Every local LLM server exposes an OpenAI-compatible API, so you can use the official OpenAI Python SDK. Zero new libraries required.

```python
from openai import OpenAI

# Point to your local server
# Ollama: http://localhost:11434/v1
# LM Studio: http://localhost:1234/v1
# llama.cpp: http://localhost:8080/v1
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="not-needed"  # Local servers don't require auth
)

# Basic chat completion
response = client.chat.completions.create(
    model="llama4-scout",
    messages=[
        {"role": "system", "content": "You are a helpful coding assistant."},
        {"role": "user", "content": "Write a Python decorator that retries failed functions with exponential backoff."}
    ],
    temperature=0.3,
    max_tokens=2048
)

print(response.choices[0].message.content)
```

### Streaming Responses

```python
from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="not-needed")

stream = client.chat.completions.create(
    model="llama4-scout",
    messages=[{"role": "user", "content": "Explain how transformers work in deep learning"}],
    stream=True
)

for chunk in stream:
    content = chunk.choices[0].delta.content
    if content:
        print(content, end="", flush=True)
print()
```

### RAG Pipeline with Local Embeddings

```python
"""
Complete local RAG pipeline — no cloud APIs involved.
Uses Ollama for both embeddings and generation.
"""
import numpy as np
from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="not-needed")


def get_embedding(text: str, model: str = "nomic-embed-text") -> list[float]:
    """Generate embeddings using a local model."""
    response = client.embeddings.create(model=model, input=text)
    return response.data[0].embedding


def cosine_similarity(a: list[float], b: list[float]) -> float:
    a, b = np.array(a), np.array(b)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


# Your knowledge base
documents = [
    "Python's GIL prevents true multi-threading for CPU-bound tasks. Use multiprocessing instead.",
    "FastAPI supports async endpoints natively and generates OpenAPI docs automatically.",
    "SQLAlchemy 2.0 uses a new query syntax with select() statements instead of the legacy Query API.",
    "Redis can be used as both a cache and a message broker for distributed systems.",
    "Docker containers share the host OS kernel, making them lighter than VMs.",
]

# Pre-compute embeddings (do this once, store in a vector DB for production)
doc_embeddings = [get_embedding(doc) for doc in documents]


def ask(question: str, top_k: int = 3) -> str:
    """Answer a question using local RAG."""
    # Step 1: Find relevant documents
    q_embedding = get_embedding(question)
    scores = [cosine_similarity(q_embedding, de) for de in doc_embeddings]
    top_indices = np.argsort(scores)[-top_k:][::-1]
    context = "\n".join(f"- {documents[i]}" for i in top_indices)

    # Step 2: Generate answer using local LLM
    response = client.chat.completions.create(
        model="llama4-scout",
        messages=[
            {
                "role": "system",
                "content": "Answer the question based on the provided context. "
                "If the context doesn't contain relevant information, say so.",
            },
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion: {question}",
            },
        ],
        temperature=0.2,
    )
    return response.choices[0].message.content


# Usage
answer = ask("How should I handle CPU-bound tasks in Python?")
print(answer)
```

### Structured Output with Local LLMs

```python
"""
Force local LLMs to output valid JSON for structured data extraction.
"""
import json
from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="not-needed")


def extract_structured_data(text: str) -> dict:
    """Extract structured data from unstructured text."""
    response = client.chat.completions.create(
        model="llama4-scout",
        messages=[
            {
                "role": "system",
                "content": (
                    "Extract information and return ONLY valid JSON. No markdown, no explanation.\n"
                    "Schema: {\"name\": str, \"email\": str|null, \"company\": str|null, "
                    "\"role\": str|null, \"sentiment\": \"positive\"|\"negative\"|\"neutral\"}"
                ),
            },
            {"role": "user", "content": text},
        ],
        temperature=0.0,
        response_format={"type": "json_object"},  # Ollama supports this
    )

    return json.loads(response.choices[0].message.content)


# Example usage
result = extract_structured_data(
    "Hi, I'm Sarah Chen from Acme Corp. I'm the VP of Engineering and I'm "
    "really impressed with your API documentation. Please reach me at sarah@acme.io"
)
print(json.dumps(result, indent=2))
# {
#   "name": "Sarah Chen",
#   "email": "sarah@acme.io",
#   "company": "Acme Corp",
#   "role": "VP of Engineering",
#   "sentiment": "positive"
# }
```

### Batch Processing with Concurrency

```python
"""
Process many prompts efficiently using async requests to a local LLM server.
"""
import asyncio
from openai import AsyncOpenAI

client = AsyncOpenAI(base_url="http://localhost:11434/v1", api_key="not-needed")

SEMAPHORE = asyncio.Semaphore(4)  # Max concurrent requests — tune for your hardware


async def process_one(prompt: str) -> str:
    async with SEMAPHORE:
        response = await client.chat.completions.create(
            model="llama4-scout",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=512,
        )
        return response.choices[0].message.content


async def batch_process(prompts: list[str]) -> list[str]:
    tasks = [process_one(p) for p in prompts]
    return await asyncio.gather(*tasks)


# Example: summarize a batch of articles
prompts = [
    f"Summarize this in one sentence: {article}"
    for article in ["Article 1 text here...", "Article 2 text here...", "Article 3 text here..."]
]

results = asyncio.run(batch_process(prompts))
for r in results:
    print(r)
```

## Docker Setup: Containerized LLM Servers

Running local LLMs in Docker is the cleanest way to deploy them as microservices — isolated, reproducible, and easy to tear down.

### Ollama in Docker

```bash
# Basic CPU-only setup
docker run -d \
  --name ollama \
  -p 11434:11434 \
  -v ollama_data:/root/.ollama \
  ollama/ollama

# With NVIDIA GPU support (requires nvidia-container-toolkit)
docker run -d \
  --name ollama-gpu \
  --gpus all \
  -p 11434:11434 \
  -v ollama_data:/root/.ollama \
  ollama/ollama

# Pull a model into the container
docker exec ollama ollama pull llama4-scout

# Test it
curl http://localhost:11434/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "llama4-scout", "messages": [{"role": "user", "content": "Hello!"}]}'
```

### Docker Compose for a Full Local AI Stack

```yaml
# docker-compose.yml
# A complete local AI stack: LLM server + vector database + web UI
version: "3.9"

services:
  ollama:
    image: ollama/ollama
    container_name: ollama
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities: [gpu]
    restart: unless-stopped

  # Open WebUI — ChatGPT-like interface for your local models
  open-webui:
    image: ghcr.io/open-webui/open-webui:main
    container_name: open-webui
    ports:
      - "3000:8080"
    environment:
      - OLLAMA_BASE_URL=http://ollama:11434
    volumes:
      - webui_data:/app/backend/data
    depends_on:
      - ollama
    restart: unless-stopped

  # ChromaDB — local vector database for RAG
  chromadb:
    image: chromadb/chroma
    container_name: chromadb
    ports:
      - "8000:8000"
    volumes:
      - chroma_data:/chroma/chroma
    restart: unless-stopped

volumes:
  ollama_data:
  webui_data:
  chroma_data:
```

```bash
# Launch the full stack
docker compose up -d

# Pull models
docker exec ollama ollama pull llama4-scout
docker exec ollama ollama pull nomic-embed-text

# Access:
# - Chat UI: http://localhost:3000
# - Ollama API: http://localhost:11434
# - ChromaDB: http://localhost:8000
```

### llama.cpp Server in Docker

```dockerfile
# Dockerfile.llamacpp
FROM ghcr.io/ggerganov/llama.cpp:server

# Models mounted at runtime via volume
ENV MODEL_PATH=/models/model.gguf

ENTRYPOINT ["llama-server", \
  "--model", "/models/model.gguf", \
  "--host", "0.0.0.0", \
  "--port", "8080", \
  "--ctx-size", "8192", \
  "--n-gpu-layers", "99", \
  "--threads", "8"]
```

```bash
# Run with a model directory mounted
docker run -d \
  --name llama-server \
  --gpus all \
  -p 8080:8080 \
  -v /path/to/your/models:/models \
  ghcr.io/ggerganov/llama.cpp:server \
  --model /models/your-model-Q4_K_M.gguf \
  --host 0.0.0.0 --port 8080 \
  --ctx-size 8192 --n-gpu-layers 99
```

## Model Comparison: Which Model for Which Task

Not all models are created equal. Here's the honest breakdown of which model to grab for each job in 2026.

### The Contenders

**Meta Llama 4 Scout** — Meta's latest open-weight release uses a Mixture-of-Experts architecture with 109B total parameters but only 17B active per forward pass. The 8B-active variant is the new default recommendation for local use. Excellent at general-purpose tasks, reasoning, and long-context work (up to 1M tokens with 16 experts). The most well-rounded model available.

**Mistral Large & Mistral 7B** — Mistral continues to punch above its weight. Mistral 7B remains the efficiency king for constrained hardware. Mistral's larger models (Mistral Large 2, Codestral) are competitive at the frontier but require serious hardware. Exceptional multilingual performance, especially for European languages.

**Microsoft Phi-4 & Phi-4 Mini** — The "small model, big brain" play. Phi-4 (14B) trained on curated high-quality data outperforms many models 3x its size on reasoning and coding benchmarks. Phi-4 Mini (3.8B) is the best model you can run on a phone or Raspberry Pi that still produces coherent, useful output. Weaknesses: creative writing and very long-form generation.

**Qwen 2.5 (7B / 14B / 32B / 72B)** — Alibaba's dark horse that's no longer a dark horse. The 7B and 14B variants are outright best-in-class for their size on coding and math. The 32B "Coder" variant is arguably the best local coding model available. Dominant for CJK language tasks. The 72B model competes with cloud frontier models on many benchmarks.

**DeepSeek-R1 (7B / 32B / 70B)** — The reasoning specialist. DeepSeek-R1 uses chain-of-thought reasoning by default, showing its work before arriving at an answer. This makes it slower (it generates more tokens) but dramatically more accurate on math, logic, science, and complex analysis. The 32B distilled variant is the sweet spot — runs on an RTX 4090 and delivers reasoning quality that punches way above its weight class.

### Decision Matrix: Which Model for Which Task

| Task | Best Model | Runner-Up | Why |
|------|-----------|-----------|-----|
| **General assistant / chat** | Llama 4 Scout 8B | Qwen 2.5 14B | Most well-rounded, fast, great instruction following |
| **Code generation** | Qwen 2.5 Coder 32B | DeepSeek-Coder-V2 | Top coding benchmarks, understands complex codebases |
| **Code review / refactoring** | DeepSeek-R1 32B | Qwen 2.5 Coder 32B | Chain-of-thought catches subtle bugs |
| **Math / logic problems** | DeepSeek-R1 32B | Qwen 2.5 32B | Built for step-by-step reasoning |
| **Creative writing** | Llama 4 Scout | Mistral 7B | Better prose, more natural voice |
| **Summarization** | Phi-4 | Llama 4 Scout 8B | Fast, accurate, efficient |
| **Data extraction / JSON** | Qwen 2.5 14B | Phi-4 | Excellent structured output compliance |
| **Multilingual (CJK)** | Qwen 2.5 14B+ | Llama 4 Scout | Trained on massive CJK corpus |
| **Multilingual (European)** | Mistral 7B | Llama 4 Scout | Mistral's strongest differentiator |
| **Edge / mobile / IoT** | Phi-4 Mini (3.8B) | Llama 3.2 3B | Best quality-per-parameter ratio |
| **RAG / retrieval** | Llama 4 Scout | Qwen 2.5 14B | Strong context-following, less hallucination |
| **Agentic / tool-use** | Qwen 2.5 32B | Llama 4 Scout | Best function-calling accuracy at this size |

### The "Just Tell Me What to Download" Guide

- **You have 8 GB RAM, no GPU:** Phi-4 Mini (3.8B Q4) — it's the only model that runs well here and still produces quality output.
- **You have 16 GB RAM or 8 GB VRAM:** Llama 4 Scout 8B-active (Q4) — the default recommendation for a reason.
- **You have 24 GB VRAM (RTX 4090):** Qwen 2.5 Coder 32B (Q4) for code, DeepSeek-R1 32B (Q4) for reasoning, Llama 4 Scout for general chat. Download all three — switching models in Ollama takes seconds.
- **You have 48+ GB VRAM or Apple Silicon with 64+ GB:** Go big. Qwen 2.5 72B or Llama 3.1 70B (Q4). You'll get cloud-competitive quality at zero marginal cost.

## Troubleshooting Common Issues

Local LLMs mostly just work in 2026, but when they don't, here's what's usually wrong.

### "Model is too slow" (< 5 tokens/sec)

**Cause:** Model is running on CPU instead of GPU, or the model is too large for your VRAM and is spilling to system RAM.

```bash
# Check if Ollama is using your GPU
ollama ps

# For NVIDIA, verify CUDA is detected
nvidia-smi

# Force GPU layers in llama.cpp (99 = all layers on GPU)
./build/bin/llama-cli -m model.gguf -ngl 99
```

**Fix:** Use a smaller model or more aggressively quantized version (Q4_K_M instead of Q6_K). If your model fits 90% in VRAM, consider Q3_K_M quantization to squeeze it in entirely — partial offloading is a performance killer.

### "Out of memory" / OOM crashes

**Cause:** Model + context window exceeds available memory.

```bash
# Reduce context size (default is often 4096 or 8192)
ollama run llama4-scout --num-ctx 2048

# In llama.cpp, set explicit context size
./build/bin/llama-cli -m model.gguf -c 2048 -ngl 99
```

**Fix:** Context window is a hidden memory hog. A 7B model at Q4 with 8K context uses about 6 GB VRAM. The same model at 32K context uses about 10 GB. Reduce context window first before switching to a smaller model.

### Ollama can't find GPU / no CUDA

```bash
# Make sure NVIDIA drivers are up to date
nvidia-smi  # Should show driver version and CUDA version

# On Linux, ensure the NVIDIA container toolkit is installed for Docker
sudo apt install nvidia-container-toolkit
sudo systemctl restart docker

# Reinstall Ollama if GPU detection fails
curl -fsSL https://ollama.com/install.sh | sh
```

### llama.cpp build fails

```bash
# Missing CUDA toolkit (NVIDIA)
sudo apt install nvidia-cuda-toolkit

# Missing Metal framework (macOS) — update Xcode command line tools
xcode-select --install

# CMake too old
pip install cmake --upgrade

# Clean rebuild
rm -rf build && cmake -B build -DGGML_CUDA=ON && cmake --build build -j$(nproc)
```

### Model outputs garbage / wrong language

**Cause:** Wrong chat template or missing system prompt.

```bash
# Ollama handles templates automatically, but for llama.cpp:
# Always specify the correct chat template
./build/bin/llama-cli -m model.gguf --chat-template llama4  # For Llama 4
./build/bin/llama-cli -m model.gguf --chat-template chatml   # For Qwen, Phi
./build/bin/llama-cli -m model.gguf --chat-template mistral  # For Mistral
```

### High memory usage even after stopping

```bash
# Ollama keeps models loaded in memory for fast switching
# Unload all models explicitly
curl http://localhost:11434/api/generate -d '{"model": "llama4-scout", "keep_alive": 0}'

# Or set a shorter keep-alive globally
export OLLAMA_KEEP_ALIVE=5m  # Unload after 5 minutes of inactivity
```

## Local LLMs vs. Cloud APIs: The Honest Comparison

Let's stop cheerleading and get real.

**Where local wins:** Privacy (absolute, no contest), cost at scale (free after hardware), latency for small models, reliability (no outages), and offline use.

**Where cloud wins:** Raw capability on frontier models, speed on 70B+ models via massive GPU clusters, zero maintenance, and cutting-edge features (vision, real-time voice, tool use at scale).

**The real answer:** Run both. Use local models for high-volume low-complexity tasks (summarization, classification, extraction, embedding), privacy-sensitive workflows, development iteration, and RAG pipelines. Use cloud APIs for tasks requiring frontier intelligence, production apps needing the absolute best quality, and one-off complex queries.

A practical split: route 80% of your inference through local models and 20% through cloud APIs. Your costs drop by 80% and your privacy surface shrinks dramatically.

## The Bottom Line

Local LLMs in 2026 aren't a compromise — they're a legitimate choice. The models are good. The tools are mature. The hardware requirements are reasonable. And now you have the installation commands, the Python code, the Docker configs, and the decision frameworks to actually ship something with them.

The open-source AI ecosystem has delivered. Meta, Mistral, Microsoft, Alibaba, Google, and DeepSeek are all shipping competitive open models. Ollama makes running them trivial. The OpenAI-compatible API means your existing code works with zero changes.

Stop renting intelligence. Start owning it.
