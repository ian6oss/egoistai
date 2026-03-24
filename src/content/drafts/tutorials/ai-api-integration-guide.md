---
title: "AI API Integration: Connect Claude, GPT, and Gemini to Your App"
excerpt: "Stop reading docs for three different APIs. Here's how to integrate Claude, GPT, and Gemini into your app with working code, real costs, and zero hand-waving."
category: "Tutorials"
categorySlug: "tutorials"
image: "/images/ai-api-integration-guide.webp"
date: "2026-03-24"
readTime: "14 min read"
author: "EgoistAI"
featured: false
tags: ["ai", "api", "claude", "gpt", "gemini", "tutorial", "python", "typescript"]
sources:
  - name: "Anthropic API Documentation"
    url: "https://docs.anthropic.com/en/api/getting-started"
  - name: "OpenAI API Reference"
    url: "https://platform.openai.com/docs/api-reference"
  - name: "Google Gemini API Documentation"
    url: "https://ai.google.dev/gemini-api/docs"
---

## Three APIs, One Guide, Zero Fluff

Every AI tutorial starts the same way: install the SDK, paste your API key, call `chat.completions.create()`, and pretend that's a real app. Then you hit streaming, tool use, error handling, and rate limits — and suddenly you're reading three different documentation sites with three different conventions, wondering why nothing works the same way twice.

This guide fixes that. We're covering Claude (Anthropic), GPT (OpenAI), and Gemini (Google) side by side. Same patterns, same structure, real code. By the end, you'll know exactly how each provider handles the things that actually matter in production.

## SDK Setup

Let's get the boring part done. All three providers have official SDKs for Python and TypeScript.

### Python

```bash
pip install anthropic openai google-genai
```

### TypeScript

```bash
npm install @anthropic-ai/sdk openai @google/genai
```

That's it. No extra dependencies, no config files. Each SDK handles HTTP, retries, and serialization internally.

## Authentication

Every provider uses API keys. Get yours from:

- **Anthropic**: [console.anthropic.com](https://console.anthropic.com/)
- **OpenAI**: [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
- **Google**: [aistudio.google.com/apikey](https://aistudio.google.com/apikey)

Set them as environment variables. Do not hardcode API keys in your source code. Ever.

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
export OPENAI_API_KEY="sk-..."
export GEMINI_API_KEY="AIza..."
```

All three SDKs auto-detect their respective environment variable, so you rarely need to pass the key explicitly.

### Python Client Initialization

```python
from anthropic import Anthropic
from openai import OpenAI
from google import genai

# All three auto-read from env vars
claude = Anthropic()
gpt = OpenAI()
gemini = genai.Client()
```

### TypeScript Client Initialization

```typescript
import Anthropic from "@anthropic-ai/sdk";
import OpenAI from "openai";
import { GoogleGenAI } from "@google/genai";

const claude = new Anthropic();
const gpt = new OpenAI();
const gemini = new GoogleGenAI();
```

Clean and consistent. All three follow the same pattern: instantiate a client, let it find the key.

## Basic Completions

Here's where the APIs start diverging. Same task — ask the model a question, get a response — but each provider structures the request differently.

### Python

```python
# --- Claude ---
response = claude.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Explain WebSockets in 3 sentences."}]
)
print(response.content[0].text)

# --- GPT ---
response = gpt.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Explain WebSockets in 3 sentences."}]
)
print(response.choices[0].message.content)

# --- Gemini ---
response = gemini.models.generate_content(
    model="gemini-2.0-flash",
    contents="Explain WebSockets in 3 sentences."
)
print(response.text)
```

### TypeScript

```typescript
// --- Claude ---
const response = await claude.messages.create({
  model: "claude-sonnet-4-20250514",
  max_tokens: 1024,
  messages: [{ role: "user", content: "Explain WebSockets in 3 sentences." }],
});
console.log(response.content[0].text);

// --- GPT ---
const response = await gpt.chat.completions.create({
  model: "gpt-4o",
  messages: [{ role: "user", content: "Explain WebSockets in 3 sentences." }],
});
console.log(response.choices[0].message.content);

// --- Gemini ---
const response = await gemini.models.generateContent({
  model: "gemini-2.0-flash",
  contents: "Explain WebSockets in 3 sentences.",
});
console.log(response.text);
```

Key differences to note:

- **Claude** requires `max_tokens`. It won't guess for you. This is actually a good design decision — you always know what you're paying for.
- **GPT** wraps the response in `choices[0].message.content`. Legacy artifact from when the API returned multiple completions.
- **Gemini** is the simplest — flat `contents` parameter, flat `.text` response. Google learned from watching the other two.

## System Prompts

All three support system-level instructions, but they handle them differently.

```python
# Claude — system is a top-level parameter
response = claude.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    system="You are a senior backend engineer. Be concise.",
    messages=[{"role": "user", "content": "Review this SQL query: SELECT * FROM users"}]
)

# GPT — system is a message role
response = gpt.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a senior backend engineer. Be concise."},
        {"role": "user", "content": "Review this SQL query: SELECT * FROM users"}
    ]
)

# Gemini — system instruction in config
response = gemini.models.generate_content(
    model="gemini-2.0-flash",
    config={"system_instruction": "You are a senior backend engineer. Be concise."},
    contents="Review this SQL query: SELECT * FROM users"
)
```

Claude's approach is the cleanest — the system prompt is structurally separate from the conversation. GPT mixes it into the message array. Gemini tucks it into a config object. All three work fine; it's just a style difference.

## Streaming

Non-negotiable for any user-facing app. Nobody wants to stare at a blank screen for 8 seconds while the model thinks. Streaming sends tokens as they're generated.

### Python

```python
# Claude
with claude.messages.stream(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Write a haiku about APIs"}]
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)

# GPT
stream = gpt.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Write a haiku about APIs"}],
    stream=True
)
for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)

# Gemini
for chunk in gemini.models.generate_content_stream(
    model="gemini-2.0-flash",
    contents="Write a haiku about APIs"
):
    print(chunk.text, end="", flush=True)
```

Claude gives you a context manager with a clean `text_stream` iterator. GPT uses a `stream=True` flag and makes you dig into `delta.content` (which can be `None`, so you need that guard). Gemini has a dedicated `generate_content_stream` method that's straightforward.

For TypeScript, the patterns mirror Python closely — Claude uses `stream()`, GPT uses `stream: true`, and Gemini uses `generateContentStream()`.

## Function Calling / Tool Use

This is where things get serious. Function calling lets the model invoke structured functions in your code — search a database, call an external API, perform calculations. It's the bridge between "chatbot" and "useful software."

### Defining Tools

```python
# Claude tool definition
claude_tools = [{
    "name": "get_weather",
    "description": "Get current weather for a city",
    "input_schema": {
        "type": "object",
        "properties": {
            "city": {"type": "string", "description": "City name"},
            "units": {"type": "string", "enum": ["celsius", "fahrenheit"]}
        },
        "required": ["city"]
    }
}]

# GPT tool definition
gpt_tools = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get current weather for a city",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "City name"},
                "units": {"type": "string", "enum": ["celsius", "fahrenheit"]}
            },
            "required": ["city"]
        }
    }
}]

# Gemini tool definition
from google.genai.types import FunctionDeclaration, Tool

gemini_tools = [Tool(function_declarations=[
    FunctionDeclaration(
        name="get_weather",
        description="Get current weather for a city",
        parameters={
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "City name"},
                "units": {"type": "string", "enum": ["celsius", "fahrenheit"]}
            },
            "required": ["city"]
        }
    )
])]
```

The schema is essentially JSON Schema across all three. The wrapping differs — GPT nests it under `function.parameters`, Claude uses `input_schema`, and Gemini uses typed classes. But the actual parameter definitions are identical.

### Handling Tool Calls

When the model decides to use a tool, you need to execute the function and feed the result back. Here's the full loop for Claude:

```python
import json

response = claude.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    tools=claude_tools,
    messages=[{"role": "user", "content": "What's the weather in Tokyo?"}]
)

# Check if the model wants to use a tool
if response.stop_reason == "tool_use":
    tool_block = next(b for b in response.content if b.type == "tool_use")

    # Execute the function (your real implementation goes here)
    result = get_weather(tool_block.input["city"])

    # Send the result back
    final = claude.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        tools=claude_tools,
        messages=[
            {"role": "user", "content": "What's the weather in Tokyo?"},
            {"role": "assistant", "content": response.content},
            {"role": "user", "content": [{
                "type": "tool_result",
                "tool_use_id": tool_block.id,
                "content": json.dumps(result)
            }]}
        ]
    )
    print(final.content[0].text)
```

GPT follows a similar loop but uses `tool_calls` on the message object and a `"tool"` role for results. Gemini uses `function_call` parts and `function_response` parts. The mental model is the same across all three: model requests a function call, you execute it, you send back the result, model generates the final response.

## Error Handling

Production code without error handling isn't production code. Here's what actually goes wrong and how to catch it.

### Python

```python
from anthropic import APIError, RateLimitError, APIConnectionError
from openai import OpenAIError, RateLimitError as OpenAIRateLimit

# Claude
try:
    response = claude.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[{"role": "user", "content": "Hello"}]
    )
except RateLimitError:
    # Back off and retry — the SDK has built-in retries, but you may want custom logic
    print("Rate limited. Waiting before retry...")
except APIConnectionError:
    print("Can't reach Anthropic API. Check your network.")
except APIError as e:
    print(f"API error: {e.status_code} — {e.message}")

# GPT
try:
    response = gpt.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": "Hello"}]
    )
except OpenAIRateLimit:
    print("Rate limited by OpenAI.")
except OpenAIError as e:
    print(f"OpenAI error: {e}")
```

All three SDKs include automatic retries with exponential backoff for transient errors (429s, 500s, connection timeouts). But don't rely on defaults blindly. Set explicit retry counts and timeouts:

```python
# Claude — configure retries
claude = Anthropic(max_retries=3, timeout=30.0)

# GPT — same pattern
gpt = OpenAI(max_retries=3, timeout=30.0)
```

## Rate Limits

Every provider throttles you. Here's the reality of what you're working with in 2026:

| Provider | Free Tier | Standard Limits | How Limits Work |
|----------|-----------|-----------------|-----------------|
| **Anthropic** | Limited usage on build tier | Varies by tier (up to thousands RPM) | Requests per minute + tokens per minute |
| **OpenAI** | Limited free credits on signup | Tier-based, scales with spend | RPM + TPM, increases automatically with usage |
| **Google** | Generous free tier for Gemini Flash | Higher limits on paid plans | RPM + TPD (tokens per day on free) |

The practical strategy is the same regardless of provider:

1. **Track your usage.** All three return usage data in response headers or the response body.
2. **Implement client-side rate limiting.** Don't just catch 429s — prevent them.
3. **Use exponential backoff.** When you do get throttled, wait 1s, then 2s, then 4s.
4. **Cache aggressively.** If you're sending the same prompt twice, you're wasting money and rate limit budget. Anthropic even offers prompt caching as a built-in feature.

```python
import time
from collections import deque

class RateLimiter:
    def __init__(self, max_requests: int, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window = window_seconds
        self.timestamps = deque()

    def wait_if_needed(self):
        now = time.time()
        while self.timestamps and self.timestamps[0] < now - self.window:
            self.timestamps.popleft()
        if len(self.timestamps) >= self.max_requests:
            sleep_time = self.timestamps[0] - (now - self.window) + 0.1
            time.sleep(sleep_time)
        self.timestamps.append(time.time())

limiter = RateLimiter(max_requests=50, window_seconds=60)

# Before each API call:
limiter.wait_if_needed()
response = claude.messages.create(...)
```

## Cost Comparison (March 2026)

Let's talk money. Pricing changes, but here's where things stand as of this writing. All prices are per million tokens.

| Model | Input | Output | Context Window |
|-------|-------|--------|----------------|
| **Claude Sonnet 4** | $3.00 | $15.00 | 200K |
| **Claude Haiku 3.5** | $0.80 | $4.00 | 200K |
| **GPT-4o** | $2.50 | $10.00 | 128K |
| **GPT-4o mini** | $0.15 | $0.60 | 128K |
| **Gemini 2.0 Flash** | $0.10 | $0.40 | 1M |
| **Gemini 2.5 Pro** | $1.25 / $2.50 | $10.00 / $15.00 | 1M |

The takeaway: **Gemini Flash is absurdly cheap** for high-volume, latency-tolerant workloads. **GPT-4o mini** is the sweet spot for OpenAI's ecosystem. **Claude Sonnet** is premium-priced but consistently produces the best structured output and follows instructions most reliably — worth it when output quality directly affects your product.

For a typical SaaS app doing 100K requests/month averaging 500 input tokens and 1,000 output tokens:

- **Gemini 2.0 Flash**: ~$45/month
- **GPT-4o mini**: ~$67/month
- **Claude Haiku 3.5**: ~$440/month
- **GPT-4o**: ~$1,125/month
- **Claude Sonnet 4**: ~$1,650/month

Don't just pick the cheapest option. Pick the cheapest option **that meets your quality bar**. A model that's 10x cheaper but produces answers your users ignore is infinitely expensive.

## Multi-Provider Architecture

Smart teams don't marry a single provider. Here's a pattern that lets you swap models without rewriting your app:

```python
from dataclasses import dataclass
from typing import Generator

@dataclass
class LLMResponse:
    text: str
    input_tokens: int
    output_tokens: int
    model: str

class LLMRouter:
    def __init__(self):
        self.claude = Anthropic()
        self.gpt = OpenAI()
        self.gemini = genai.Client()

    def complete(self, prompt: str, provider: str = "claude",
                 model: str | None = None) -> LLMResponse:
        if provider == "claude":
            model = model or "claude-sonnet-4-20250514"
            r = self.claude.messages.create(
                model=model, max_tokens=1024,
                messages=[{"role": "user", "content": prompt}]
            )
            return LLMResponse(
                text=r.content[0].text,
                input_tokens=r.usage.input_tokens,
                output_tokens=r.usage.output_tokens,
                model=model
            )
        elif provider == "openai":
            model = model or "gpt-4o"
            r = self.gpt.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}]
            )
            return LLMResponse(
                text=r.choices[0].message.content,
                input_tokens=r.usage.prompt_tokens,
                output_tokens=r.usage.completion_tokens,
                model=model
            )
        elif provider == "gemini":
            model = model or "gemini-2.0-flash"
            r = self.gemini.models.generate_content(
                model=model, contents=prompt
            )
            return LLMResponse(
                text=r.text,
                input_tokens=r.usage_metadata.prompt_token_count,
                output_tokens=r.usage_metadata.candidates_token_count,
                model=model
            )

router = LLMRouter()

# Easy to switch or A/B test
response = router.complete("Summarize this document...", provider="gemini")
```

This pattern gives you three superpowers: failover (if one provider is down, route to another), cost optimization (use cheap models for simple tasks, premium models for hard ones), and A/B testing (compare output quality across providers with real traffic).

## What You Should Build Next

You now have working code for all three major AI APIs. Here's where to go from here:

1. **Build the router pattern above** and benchmark all three providers against your actual use case. Synthetic benchmarks lie. Your data is the only truth.
2. **Implement streaming first.** If your app has a UI, non-streaming responses feel broken in 2026. Users expect to see tokens appear in real time.
3. **Add tool use for anything that needs real data.** The moment your AI needs current information — prices, weather, user data — function calling is the answer. RAG is the other answer, but that's a different article.
4. **Set up cost tracking from day one.** Log every request with its token count and cost. You'll thank yourself when your bill spikes and you need to figure out which endpoint is burning money.

The AI API landscape moves fast, but the fundamentals — authentication, completions, streaming, tool use, error handling — stay remarkably stable. Learn the patterns once, and you'll adapt to whatever comes next without breaking a sweat.
