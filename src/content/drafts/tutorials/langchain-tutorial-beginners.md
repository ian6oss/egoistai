---
title: "LangChain Tutorial for Beginners: Build AI Agents"
excerpt: "LangChain lets you build AI agents that use tools, search the web, and chain reasoning steps. This tutorial takes you from zero to a working agent in under an hour."
category: "Tutorials"
categorySlug: "tutorials"
image: "/images/langchain-tutorial-beginners.webp"
date: "2026-03-26"
readTime: "14 min read"
author: "EgoistAI"
featured: false
tags: ["langchain", "ai agents", "tutorial", "python", "llm", "openai", "claude", "beginners"]
sources:
  - name: "LangChain Documentation"
    url: "https://python.langchain.com/docs/introduction/"
  - name: "LangChain GitHub Repository"
    url: "https://github.com/langchain-ai/langchain"
  - name: "LangSmith Documentation"
    url: "https://docs.smith.langchain.com/"
---

## What Is LangChain and Why Should You Learn It?

LangChain is a Python (and JavaScript) framework for building applications powered by large language models. It solves the biggest pain point of working with LLMs: connecting them to the real world. Out of the box, models like GPT-4.5 and Claude can only process text you feed them. LangChain gives them tools — web search, database access, file reading, API calls, code execution — and the ability to chain multiple reasoning steps into a coherent workflow. If you've ever wanted to build an AI that can "research a topic, summarize the findings, and email them to you," LangChain is how you do it. This tutorial covers LangChain v0.3 (the current stable release), walks you through building three real projects, and doesn't assume you've ever touched LangChain before. You need basic Python knowledge — that's it.

## What Can You Build with LangChain?

Before we write code, here's what LangChain is actually good for:

- **AI agents** that use tools (search, calculate, browse websites)
- **RAG applications** that answer questions from your own documents
- **Chatbots** with memory that remember previous conversations
- **Data analysis pipelines** that query databases and summarize results
- **Content generation workflows** with multi-step editing and review
- **Automation agents** that interact with APIs, send emails, and manage tasks

What LangChain is *not* good for: simple one-shot API calls to an LLM. If you just need to send a prompt and get a response, use the OpenAI or Anthropic SDK directly. LangChain adds overhead that's only justified when you need chaining, tools, or memory.

## How Do You Set Up LangChain?

### Step 1: Install Dependencies

```bash
pip install langchain langchain-openai langchain-anthropic langchain-community
pip install python-dotenv tavily-python
```

### Step 2: Set Up API Keys

Create a `.env` file in your project root:

```
OPENAI_API_KEY=sk-your-openai-key
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key
TAVILY_API_KEY=tvly-your-tavily-key
```

Tavily is a search API built specifically for AI agents. Free tier gives you 1,000 searches/month — plenty for learning.

### Step 3: Verify Installation

```python
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(model="gpt-4o")
response = llm.invoke("Say hello in three languages")
print(response.content)
```

If you see a response, you're good. Let's build.

## Project 1: How Do You Build a Simple Chatbot with Memory?

Most LLM interactions are stateless — the model doesn't remember what you said two messages ago. LangChain fixes this with conversation memory.

```python
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

load_dotenv()

llm = ChatOpenAI(model="gpt-4o")

# Store for session histories
store = {}

def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

# Create a chain with message history
chain_with_history = RunnableWithMessageHistory(
    llm,
    get_session_history,
)

# Configuration for the session
config = {"configurable": {"session_id": "user_123"}}

# First message
response1 = chain_with_history.invoke(
    [HumanMessage(content="Hi, my name is Alex and I'm building a fitness app")],
    config=config,
)
print(response1.content)

# Second message — the model remembers the context
response2 = chain_with_history.invoke(
    [HumanMessage(content="What tech stack would you recommend for my project?")],
    config=config,
)
print(response2.content)
```

The key insight: `RunnableWithMessageHistory` automatically appends previous messages to each new request. The model sees the full conversation history and responds in context. The `session_id` lets you maintain separate conversations for different users.

### LangChain Memory Options Compared

| Memory Type | How It Works | Best For | Limitations |
|-------------|-------------|----------|-------------|
| InMemoryChatMessageHistory | Stores all messages in RAM | Prototyping, short sessions | Lost on restart, RAM-bound |
| RedisChatMessageHistory | Stores in Redis | Production, multi-server | Requires Redis setup |
| SQLChatMessageHistory | Stores in SQL database | Persistent storage | Slightly slower |
| ConversationBufferWindowMemory | Keeps last N messages | Long conversations | Older context lost |
| ConversationSummaryMemory | Summarizes older messages | Very long sessions | Lossy compression |

For production apps, use Redis or SQL. For learning, `InMemoryChatMessageHistory` is perfect.

## Project 2: How Do You Build an AI Agent with Tools?

This is where LangChain earns its keep. We're going to build an agent that can search the web, do math, and answer questions using real-time information.

```python
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

load_dotenv()

# Initialize the LLM
llm = ChatOpenAI(model="gpt-4o")

# Tool 1: Web search
search_tool = TavilySearchResults(max_results=3)

# Tool 2: Custom calculator
@tool
def calculator(expression: str) -> str:
    """Evaluate a mathematical expression. Use this for any math calculations."""
    try:
        result = eval(expression)  # In production, use a safe math parser
        return str(result)
    except Exception as e:
        return f"Error: {e}"

# Tool 3: Custom tool — get current date
@tool
def get_current_date() -> str:
    """Get today's date. Use this when you need the current date."""
    from datetime import date
    return date.today().isoformat()

# Create the agent
tools = [search_tool, calculator, get_current_date]
agent = create_react_agent(llm, tools)

# Run the agent
result = agent.invoke({
    "messages": [
        ("human", "What's the current stock price of NVIDIA and what's its market cap divided by revenue?")
    ]
})

# Print the agent's response
for message in result["messages"]:
    if hasattr(message, 'content') and message.content:
        print(f"{message.type}: {message.content}\n")
```

What happens behind the scenes:
1. The agent receives your question
2. It decides it needs to search for NVIDIA's stock price — calls `search_tool`
3. It extracts the price and revenue numbers from search results
4. It calls `calculator` to compute market cap / revenue
5. It formats a final answer with all the pieces

This is the **ReAct pattern** (Reasoning + Acting): the model reasons about what to do, takes an action (calls a tool), observes the result, and repeats until it has enough information to answer.

### How Do You Create Custom Tools?

The `@tool` decorator is the easiest way:

```python
@tool
def query_database(sql: str) -> str:
    """Execute a SQL query against the analytics database.
    Use this when you need to look up user metrics, revenue data,
    or any analytics information."""
    import sqlite3
    conn = sqlite3.connect("analytics.db")
    cursor = conn.execute(sql)
    results = cursor.fetchall()
    conn.close()
    return str(results)
```

The docstring matters — it's what the LLM reads to decide when to use the tool. Be specific about what the tool does and when it should be used.

## Project 3: How Do You Build a RAG Application?

RAG (Retrieval-Augmented Generation) lets your AI answer questions from your own documents. This is the single most common LangChain use case in production.

```python
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

load_dotenv()

# Step 1: Load documents
loader = PyPDFLoader("company_handbook.pdf")
documents = loader.load()

# Step 2: Split into chunks
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
)
chunks = splitter.split_documents(documents)

# Step 3: Create embeddings and store in vector database
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vectorstore = Chroma.from_documents(chunks, embeddings, persist_directory="./chroma_db")
retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

# Step 4: Create the RAG chain
template = """Answer the question based only on the following context.
If the context doesn't contain the answer, say "I don't have that information."

Context:
{context}

Question: {question}

Answer:"""

prompt = ChatPromptTemplate.from_template(template)
llm = ChatOpenAI(model="gpt-4o")

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
)

# Step 5: Query
answer = rag_chain.invoke("What is the company's remote work policy?")
print(answer.content)
```

### RAG Architecture Breakdown

Here's what each component does:

1. **Document Loader**: Reads your files (PDF, TXT, CSV, web pages, etc.)
2. **Text Splitter**: Breaks documents into chunks that fit in the LLM's context window
3. **Embeddings**: Converts text chunks into numerical vectors for similarity search
4. **Vector Store**: Stores and indexes the vectors (Chroma, Pinecone, Weaviate)
5. **Retriever**: Finds the most relevant chunks for a given question
6. **LLM + Prompt**: Takes the retrieved chunks and generates an answer

### Which Vector Database Should You Use with LangChain?

| Vector Database | Setup Complexity | Cost | Best For |
|----------------|------------------|------|----------|
| Chroma | Very easy (local) | Free | Prototyping, small datasets |
| FAISS | Easy (local) | Free | Large local datasets |
| Pinecone | Easy (cloud) | Free tier + paid | Production, managed service |
| Weaviate | Medium | Free (self-hosted) | Production, hybrid search |
| Qdrant | Medium | Free (self-hosted) | Production, performance |
| pgvector | Easy (if using Postgres) | Free | Existing Postgres users |

Start with Chroma for learning, move to Pinecone or Qdrant for production.

## LangChain vs Alternatives: Which Framework Should You Choose?

LangChain isn't the only option. Here's an honest comparison:

| Framework | Strengths | Weaknesses | Best For |
|-----------|-----------|------------|----------|
| LangChain | Largest ecosystem, most integrations | Complex, over-abstracted at times | Full-featured AI applications |
| LlamaIndex | Best for RAG specifically | Less flexible for agents | Document Q&A systems |
| CrewAI | Best multi-agent framework | Narrower scope | Multi-agent collaboration |
| Haystack | Clean architecture, production-ready | Smaller community | Enterprise RAG |
| Raw SDKs | Maximum control, no overhead | More code for common patterns | Simple applications |

If you're building a RAG app, LlamaIndex might be simpler. If you're building multi-agent systems, CrewAI is more specialized. But if you want one framework that does everything — agents, RAG, memory, chains — LangChain is still the default choice.

## What Are Common LangChain Mistakes to Avoid?

1. **Over-engineering simple tasks**: If you just need to call an API and get a response, use the raw SDK. LangChain adds value when you need chaining, tools, or memory.

2. **Ignoring LangSmith**: LangSmith (LangChain's tracing/debugging tool) is free for development and invaluable for understanding why your agent made weird decisions. Set it up from day one.

3. **Huge chunks in RAG**: Don't set chunk_size to 5000. Smaller chunks (500-1000 tokens) with overlap produce better retrieval results.

4. **Not testing tools**: Your agent is only as good as its tools. If a tool returns garbage, the agent produces garbage. Test each tool independently before giving it to the agent.

5. **Skipping error handling**: Agents can get stuck in loops, call tools with wrong arguments, or hit rate limits. Implement max iterations and proper error handling.

If you're experimenting with multiple LLM providers for your LangChain projects — comparing GPT-4o vs Claude vs Gemini for your specific use case — [GamsGo](https://www.gamsgo.com/partner/uZJ7x) offers discounted access to premium AI subscriptions so you can test without burning through full-price API credits.

## What Are the Next Steps After This Tutorial?

1. **LangGraph**: LangChain's framework for building stateful, multi-step agents with branching logic. It's the evolution of LangChain's agent framework.
2. **LangSmith**: Set up tracing to debug and optimize your chains.
3. **Production deployment**: Use LangServe to deploy your chains as REST APIs.
4. **Advanced RAG**: Explore hybrid search, re-ranking, and query decomposition.
5. **Multi-agent systems**: Build systems where multiple agents collaborate on complex tasks.

## FAQ

### Is LangChain free?
Yes, LangChain is open-source and free to use. You pay for the LLM API calls (OpenAI, Anthropic, etc.) and any cloud services (vector databases, hosting). LangSmith has a free tier for development.

### Do I need to know Python to use LangChain?
Basic Python is sufficient — variables, functions, classes, and package management. You don't need advanced Python skills. LangChain also has a JavaScript/TypeScript version (LangChain.js) if that's your preference.

### Can I use LangChain with local models?
Yes. LangChain integrates with Ollama, llama.cpp, and Hugging Face Transformers. You can run Llama 4, Mistral, or any open-source model locally and use it with LangChain's full feature set.

### Is LangChain production-ready?
Yes, with caveats. Many companies run LangChain in production (Elastic, Robinhood, Rakuten). The key is to use LangChain's stable interfaces, implement proper error handling, and monitor with LangSmith. Avoid using experimental features in production.

### What's the difference between LangChain and LangGraph?
LangChain provides the building blocks (LLMs, tools, prompts, memory). LangGraph is a higher-level framework built on LangChain for creating complex, stateful agents with branching logic and cycles. Think of LangChain as the foundation and LangGraph as the architecture framework on top.

### How do LangChain agents handle errors?
By default, if a tool call fails, the error message is passed back to the LLM, which can retry or try a different approach. You can configure max iterations (to prevent infinite loops), fallback strategies, and custom error handling. Always set `max_iterations` in production to prevent runaway agents.