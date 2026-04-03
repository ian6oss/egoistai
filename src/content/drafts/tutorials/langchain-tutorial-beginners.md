---
title: "LangChain Tutorial for Beginners: Build AI Agents That Actually Work"
excerpt: "Tired of dumb LLMs? Learn LangChain. This guide cuts the crap, showing you how to build real AI agents with tools, memory, and actual intelligence. No fluff, just code."
category: "Tutorials"
categorySlug: "tutorials"
image: "/images/langchain-tutorial-beginners.webp"
date: "2026-04-03"
readTime: "12 min read"
author: "EgoistAI"
featured: false
tags: ["LangChain", "AI agents", "Python tutorial", "LLM development", "AI programming", "Generative AI"]
sources:
  - name: "LangChain Documentation"
    url: "https://python.langchain.com/docs/get_started/introduction"
  - name: "OpenAI API Documentation"
    url: "https://platform.openai.com/docs/overview"
  - name: "ReAct: Synergizing Reasoning and Acting in Language Models"
    url: "https://react-lm.github.io/"
  - name: "LangChain Blog - Chains vs. Agents"
    url: "https://blog.langchain.dev/chains-vs-agents/"
  - name: "Wikipedia API - Python client"
    url: "https://pypi.org/project/wikipedia-api/"
---

Sick of your LLMs acting like glorified autocomplete machines? You feed them a prompt, they spit out text. Repeat. It's like talking to a genius with amnesia and no hands. If you want AI that can *think*, *act*, and *remember*, you need to graduate from mere prompt engineering to building AI agents. And for that, you need LangChain.

Forget the marketing fluff. LangChain isn't magic. It's a pragmatic, powerful framework that gives your Large Language Models (LLMs) the tools and structure they need to become intelligent agents. We're talking about systems that can decide what to do, use external tools (like search engines or APIs), process information, and maintain context over a conversation.

This isn't another "hello world" tutorial that leaves you wondering what to do next. We're cutting straight to the chase. By the end of this guide, you'll have built a functional AI agent that can actually *do* things, not just parrot back pre-programmed responses. Let's get to work.

## What is LangChain, Really, Beyond the Hype?

Let's be blunt: a raw LLM is powerful, but it's also blind, deaf, and mute to the outside world. It knows what it was trained on, and that's it. It can't search the web for current events, access your company database, or execute code. It can't even remember what you said two turns ago without explicit instruction.

LangChain is an open-source framework designed to bridge this gap. It provides a structured way to:

1.  **Connect LLMs to Data Sources:** Think of Retrieval Augmented Generation (RAG) – giving your LLM access to vast external knowledge bases.
2.  **Allow LLMs to Interact with Their Environment:** This is where "agents" come in. LangChain lets your LLM use *tools* – search engines, calculators, custom APIs – to gather information and take actions.
3.  **Manage Complex LLM Workflows:** Orchestrate multiple prompts, LLM calls, and tool usages into coherent "chains" or "agents."
4.  **Give LLMs Memory:** Ensure your LLM remembers past interactions, providing conversational context.

In essence, LangChain isn't about making the LLM smarter itself. It's about giving the LLM the sensory organs, limbs, and short-term memory it needs to appear intelligent and actually *do useful tasks* in the real world.

## Why Bother with LangChain When I Can Just Prompt OpenAI Directly?

Good question. If all you're doing is sending a single prompt and getting a single response, you probably don't *need* LangChain. But that's like using a supercar to drive to the corner store. It's overkill and misses the point.

You bother with LangChain when:

*   **Your LLM needs current information:** Raw LLMs are often several months or even years out of date.
*   **Your LLM needs to perform calculations:** LLMs are terrible at math.
*   **Your LLM needs to interact with external systems:** Databases, APIs, local files, your company's CRM.
*   **Your AI application involves multi-step reasoning:** The LLM needs to break down a complex problem, use tools, process results, and then synthesize a final answer.
*   **You need conversational memory:** Your AI application should remember what was discussed earlier in a session.
*   **You want to build robust, scalable AI applications:** LangChain provides abstractions that make your code cleaner, more modular, and easier to maintain than a spaghetti mess of raw API calls and string parsing.

If you're building anything beyond a glorified chatbot that regurgitates pre-canned responses, LangChain is your foundational toolkit. It turns your LLM from a passive text generator into an active problem-solver.

## Getting Started: The Setup – Ditch the Fluff, Get to Code

Before we write any fancy agent logic, we need to set up our environment. No excuses, let's get this done.

### What Do You Need to Install?

First, ensure you have Python 3.9+ installed. Then, fire up your terminal.

```bash
# Create a virtual environment (highly recommended)
python -m venv venv
source venv/bin/activate # On Windows, use `venv\Scripts\activate`

# Install LangChain and the OpenAI integration
pip install langchain-openai python-dotenv

# For our agent, we'll need a couple of tools
pip install wikipedia duckduckgo-search
```

### How Do You Handle API Keys Without Exposing Them?

Don't be an idiot and hardcode your API keys. Seriously. Use environment variables. We installed `python-dotenv` for a reason.

1.  **Get your OpenAI API key:** If you don't have one, sign up at [platform.openai.com](https://platform.openai.com/docs/overview) and create a new secret key. Remember, they charge for usage. Don't go wild.
2.  **Create a `.env` file:** In the root of your project directory, create a file named `.env`.
3.  **Add your key:** Inside `.env`, add the following line:

    ```
    OPENAI_API_KEY="your_openai_api_key_here"
    ```
    Replace `"your_openai_api_key_here"` with your actual key.

Now, whenever you run a Python script from this directory, `python-dotenv` will load this key into your environment variables, making it accessible to LangChain without being exposed in your code.

## The Core Components: Your Agent's Toolbox – What Are We Working With?

LangChain breaks down complex LLM applications into modular components. Understanding these is crucial.

### What's the Difference Between LLMs and ChatModels?

At their core, LangChain interacts with large language models. But LangChain differentiates between two main types:

*   **`LLM`:** These are traditional text completion models (e.g., older GPT-3 models). You give them a string, they complete it.
*   **`ChatModel`:** These are optimized for conversational turns (e.g., GPT-3.5-turbo, GPT-4). You provide a list of messages (user, system, assistant), and they respond with a message. For most modern agent-based applications, **you'll be using `ChatModel`**.

We'll use `ChatOpenAI` which is a `ChatModel` for our project.

### Why Do We Need Prompt Templates?

Typing out raw strings for every LLM interaction is inefficient and error-prone. **Prompt Templates** are like f-strings for your LLM prompts. They allow you to define a prompt structure with placeholders for dynamic input.

```python
from langchain_core.prompts import ChatPromptTemplate

template = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Your name is {name}."),
    ("user", "Hello, my name is {user_name}. What is yours?"),
])

prompt = template.format_messages(name="EgoistAI Assistant", user_name="Alice")
print(prompt)
# Output:
# [HumanMessage(content='Hello, my name is Alice. What is yours?'), SystemMessage(content='You are a helpful assistant. Your name is EgoistAI Assistant.')]
```
Notice how `format_messages` returns a list of `Message` objects, perfect for `ChatModel`s.

### What are Output Parsers and Why Are They Essential?

LLMs output raw text. Often, you need that text in a structured format (e.g., JSON, a specific Python object). **Output Parsers** take the LLM's raw string output and transform it into something usable by your application.

The simplest is `StrOutputParser`, which just returns the raw string. More advanced parsers can enforce JSON schemas or Pydantic models.

### How Do Chains Link Things Together?

**Chains** are sequences of calls – to LLMs, to other chains, or to tools. They allow you to combine multiple components into a single, coherent workflow. Think of them as pipelines.

A simple chain might be: `Prompt Template -> LLM -> Output Parser`.

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 1. Load your API key from .env
from dotenv import load_dotenv
import os
load_dotenv()

# 2. Define your LLM
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# 3. Define your prompt
prompt = ChatPromptTemplate.from_template("Tell me a short joke about {topic}.")

# 4. Define your output parser
output_parser = StrOutputParser()

# 5. Create the chain
joke_chain = prompt | llm | output_parser

# 6. Run the chain
print(joke_chain.invoke({"topic": "AI"}))
# Example Output: Why did the AI break up with the internet? It had too many emotional attachments to its data!
```

This `|` syntax is the LangChain Expression Language (LCEL), a powerful and concise way to build chains.

### What Exactly Are Agents and How Do They Work?

This is where the real intelligence kicks in. An **Agent** is an LLM that can **reason** about *what to do* based on a user's input, and then **act** by using a set of available **tools**.

Here's the workflow:

1.  **User Input:** You ask the agent a question or give it a task.
2.  **LLM Reasoning:** The agent's LLM component analyzes the input and its available tools. It thinks: "What steps do I need to take to fulfill this request? Which tools are relevant?"
3.  **Tool Selection:** Based on its reasoning, the LLM decides which tool to use and what input to give it.
4.  **Tool Execution:** The selected tool is executed.
5.  **Observation:** The agent receives the output from the tool.
6.  **Loop:** The LLM then re-evaluates: "Did the tool's output help me solve the problem? Do I need another tool? Am I done?" This process repeats until the agent believes it has a final answer or reaches a stopping condition.

The most common agent architecture is **ReAct** (Reasoning and Acting), which interleaves reasoning steps (what to think) with acting steps (what tool to use, what observation resulted).

### What are Tools and Why Are They So Crucial?

**Tools** are functions that your agent can call to interact with the outside world. Without tools, an agent is just a chain. With tools, it gains superpowers.

Examples of tools:

*   **Search Engine:** Google Search, DuckDuckGo, Wikipedia (for up-to-date information).
*   **Calculator:** For precise numerical computations.
*   **API Wrapper:** Accessing any external service (weather API, stock market API, internal databases).
*   **Code Interpreter:** Executing Python code to perform complex data manipulation or analysis.
*   **File System Access:** Reading or writing files.

LangChain provides many pre-built tools, and you can easily create custom ones.

### How Can Agents Remember Things with Memory?

By default, an agent is stateless. Each interaction is a fresh start. **Memory** components allow an agent to recall previous interactions, maintaining conversational context across turns.

Common memory types:

*   **`ConversationBufferMemory`:** Stores all previous messages directly. Simple, but can grow large.
*   **`ConversationSummaryMemory`:** Summarizes past conversations to save space.
*   **`ConversationBufferWindowMemory`:** Stores only the last `k` interactions.

Memory is integrated into the `AgentExecutor` (which is the runtime for your agent).

## LangChain vs. Direct LLM Calls: What's the Real Difference?

Let's put this into perspective. Why bother with all these components when you could just hit the OpenAI API directly?

| Feature             | Direct LLM API Call                                 | LangChain Framework                                        |
| :------------------ | :-------------------------------------------------- | :--------------------------------------------------------- |
| **Complexity**      | Simple for single turn, rapidly complex for multi-step | Higher initial setup, simpler for complex flows            |
| **External Tools**  | Requires manual integration, parsing, and looping   | Native tool integration and decision-making (Agents)       |
| **Context/Memory**  | Manual management of message history                | Built-in memory modules for various strategies             |
| **Modularity**      | Low, often monolithic prompt-response logic         | High, components (LLMs, Prompts, Tools, Chains) are interchangeable |
| **Orchestration**   | Manual conditional logic and state management       | Abstracted via Chains and Agents, simpler flow control     |
| **Maintenance**     | Difficult to scale, prone to "prompt spaghetti"     | Easier to debug and maintain due to clear component separation |
| **Learning Curve**  | Low for basics, steep for advanced applications     | Moderate for basics, smoother for advanced features        |
| **Use Case**        | Simple text generation, classification              | Multi-turn conversations, data retrieval, task automation, complex agents |

The bottom line? If you're building anything that needs to be robust, adaptable, and genuinely intelligent, LangChain is the pragmatic choice.

## The Main Event: Building Your First Agent – "The Smart Research Assistant"

Let's get our hands dirty. We're going to build a research assistant agent. This agent will be able to answer questions by intelligently deciding whether to use a general web search (DuckDuckGo) or a specific knowledge base (Wikipedia).

### What's the Goal of Our Research Assistant?

Our agent will:

1.  Receive a user's question (e.g., "Who won the World Series in 2023?").
2.  Analyze the question.
3.  Decide which tool (Wikipedia or DuckDuckGo Search) is best suited to answer it.
4.  Execute the chosen tool.
5.  Synthesize the tool's output into a coherent answer.
6.  Handle cases where it doesn't know the answer.

### Step 1: Define Your Tools – Giving Your Agent Capabilities

Remember, an agent is only as good as its tools. For our research assistant, we need two: Wikipedia and DuckDuckGo Search.

```python
from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper

# Initialize Wikipedia tool
wikipedia_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=1000)
wikipedia_tool = WikipediaQueryRun(api_wrapper=wikipedia_wrapper)

# Initialize DuckDuckGo Search tool
duckduckgo_search_tool = DuckDuckGoSearchRun()

# Package them into a list
tools = [wikipedia_tool, duckduckgo_search_tool]
```
Each tool has a `name` (e.g., "Wikipedia", "DuckDuckGo Search") and a `description`. The LLM uses these descriptions to decide which tool is appropriate for a given task. Make your descriptions clear and concise!

### Step 2: Initialize the LLM – The Brain of Your Agent

We'll use `ChatOpenAI` as the agent's brain. For agents, a lower `temperature` (closer to 0) is generally preferred for more deterministic and logical reasoning.

```python
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv() # Load API key from .env

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
```

### Step 3: Create the Agent – Connecting Brain and Tools

Now, we combine the LLM and the tools into an agent. We'll use `create_react_agent` because ReAct (Reasoning and Acting) is a robust and widely used architecture for agents.

We also need a prompt for the agent. This prompt instructs the LLM on its role, the tools it has, and how to use them. LangChain provides a default prompt for ReAct agents, but you can customize it.

```python
from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent

# Get the prompt from LangChain Hub
# This is a standard ReAct prompt that tells the LLM how to use tools
prompt = hub.pull("hwchase17/react")

# Create the agent
agent = create_react_agent(llm, tools, prompt)

# Create the AgentExecutor
# This is the runtime for the agent, which handles the looping of reasoning and tool calls
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)
```
*   `hub.pull("hwchase17/react")`: LangChain Hub is a repository of shared LangChain components. This pulls a well-tested prompt template specifically designed for ReAct agents.
*   `create_react_agent`: This function takes your LLM, tools, and the ReAct prompt to construct the agent logic.
*   `AgentExecutor`: This is the engine that runs the agent.
    *   `verbose=True`: Crucial for debugging! It prints out the agent's thought process, tool calls, and observations.
    *   `handle_parsing_errors=True`: Helps the agent recover from errors in its own output, making it more robust.

### Step 4: Run the Agent – Unleash the Power

Now, let's ask our agent a question!

```python
# Run the agent
print("--- Agent Running ---")
response = agent_executor.invoke({"input": "What is the capital of France?"})
print("\n--- Agent Response ---")
print(response["output"])

print("\n--- Agent Running ---")
response = agent_executor.invoke({"input": "Who was the first person to walk on the moon and when did it happen?"})
print("\n--- Agent Response ---")
print(response["output"])

print("\n--- Agent Running ---")
response = agent_executor.invoke({"input": "What is the current population of Tokyo?"})
print("\n--- Agent Response ---")
print(response["output"])
```

When you run this, pay close attention to the `verbose` output. You'll see the agent's `Thought`, `Action`, `Action Input`, and `Observation` steps. This is the ReAct pattern in action. It's the LLM actively deciding, executing, and learning.

### Full Code Example: Your Smart Research Assistant

```python
import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent

# 1. Load environment variables (API keys)
load_dotenv()

# 2. Initialize LLM (the brain)
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# 3. Define Tools (the capabilities)
wikipedia_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=1000)
wikipedia_tool = WikipediaQueryRun(api_wrapper=wikipedia_wrapper)

duckduckgo_search_tool = DuckDuckGoSearchRun()

tools = [wikipedia_tool, duckduckgo_search_tool]

# 4. Get the Agent Prompt
# This prompt guides the LLM on how to reason and use tools
prompt = hub.pull("hwchase17/react")

# 5. Create the Agent
# Combines the LLM, tools, and prompt into a decision-making entity
agent = create_react_agent(llm, tools, prompt)

# 6. Create the Agent Executor
# This is the runtime that executes the agent's decisions
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True, # Set to True to see the agent's thought process
    handle_parsing_errors=True # Helps recover from potential LLM output errors
)

# 7. Run the Agent with some questions
print("--- Running Agent: What is the capital of France? ---")
response1 = agent_executor.invoke({"input": "What is the capital of France?"})
print("\nAgent Response:", response1["output"])

print("\n--- Running Agent: Who was the first person to walk on the moon and when did it happen? ---")
response2 = agent_executor.invoke({"input": "Who was the first person to walk on the moon and when did it happen?"})
print("\nAgent Response:", response2["output"])

print("\n--- Running Agent: What is the current population of Tokyo? ---")
response3 = agent_executor.invoke({"input": "What is the current population of Tokyo?"})
print("\nAgent Response:", response3["output"])

print("\n--- Running Agent: What is the square root of 123456789? ---")
response4 = agent_executor.invoke({"input": "What is the square root of 123456789?"})
print("\nAgent Response:", response4["output"]) # Expect it to try searching, but might struggle without a calculator tool

print("\n--- Running Agent: Tell me a joke about AI. ---")
response5 = agent_executor.invoke({"input": "Tell me a joke about AI."})
print("\nAgent Response:", response5["output"]) # Should answer directly without tools
```

When you run `response4`, you'll likely see the agent try to use DuckDuckGo or Wikipedia, realize it can't *calculate* the square root, and then either give a general answer or state it can't perform the calculation. This highlights the importance of having the *right* tools. If we had a `MathTool`, it would use it.

## Adding Persistence: Giving Your Agent a Memory – Why Does It Keep Forgetting?

Our current agent is brilliant, but it's got the memory of a goldfish. Each `invoke` call is a new interaction. If you ask it "What's my name?" and then "What's my favorite color?", it won't remember your name from the previous turn. For conversational agents, this is a deal-breaker.

### Why Do Agents Need Memory?

*   **Context:** To understand follow-up questions or references to previous parts of the conversation.
*   **Personalization:** To remember user preferences or facts about the user.
*   **Coherence:** To maintain a natural, flowing dialogue.

### How Do You Integrate Memory into an Agent?

We'll use `ConversationBufferMemory`, the simplest form of memory, which just stores all previous messages.

```python
import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from langchain.memory import ConversationBufferMemory # Import Memory

# 1. Load environment variables
load_dotenv()

# 2. Initialize LLM
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# 3. Define Tools
wikipedia_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=1000)
wikipedia_tool = WikipediaQueryRun(api_wrapper=wikipedia_wrapper)
duckduckgo_search_tool = DuckDuckGoSearchRun()
tools = [wikipedia_tool, duckduckgo_search_tool]

# 4. Get the Agent Prompt
# For agents with memory, the prompt needs to include `chat_history`
prompt = hub.pull("hwchase17/react-chat") # Use the chat-specific ReAct prompt

# 5. Initialize Memory
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# 6. Create the Agent
# The agent now knows about `chat_history` from the prompt
agent = create_react_agent(llm, tools, prompt)

# 7. Create the Agent Executor with Memory
agent_executor_with_memory = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    memory=memory, # Pass the memory object here
    handle_parsing_errors=True
)

# 8. Run the Agent with a conversational flow
print("--- Running Agent with Memory: First Turn ---")
response_mem1 = agent_executor_with_memory.invoke({"input": "My name is Alex. What's the capital of Spain?"})
print("\nAgent Response:", response_mem1["output"])

print("\n--- Running Agent with Memory: Second Turn ---")
response_mem2 = agent_executor_with_memory.invoke({"input": "What's my name?"})
print("\nAgent Response:", response_mem2["output"])

print("\n--- Running Agent with Memory: Third Turn ---")
response_mem3 = agent_executor_with_memory.invoke({"input": "And who painted 'Guernica'?"})
print("\nAgent Response:", response_mem3["output"])
```
Notice the change in the prompt: `hub.pull("hwchase17/react-chat")`. This specific prompt template is designed to include `chat_history` as an input variable for the LLM, allowing it to "see" past interactions. By passing the `memory` object to `AgentExecutor`, it automatically manages injecting and retrieving conversation history.

Now, your agent remembers "Alex" from the first turn! This is a fundamental step towards building truly interactive and intelligent AI applications.

## Beyond the Basics: What's Next for Your AI Agents?

You've built a basic, functional AI agent. Congratulations. But don't stop there. LangChain is a deep rabbit hole, and there's much more to explore:

*   **Custom Tools:** Learn to create your own tools to interact with *any* API or system. This is where your agents become truly unique and powerful for specific business needs.
*   **Retrieval Augmented Generation (RAG):** Integrate vector databases (like Chroma