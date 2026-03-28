---
title: "MCP Servers Tutorial: Connect AI to Everything"
excerpt: "Stop copy-pasting context into ChatGPT. MCP servers let Claude talk directly to your files, databases, APIs, and tools. Here's how to set it up."
category: "Tutorials"
categorySlug: "tutorials"
image: "/images/mcp-servers-tutorial.webp"
date: "2026-03-28"
readTime: "12 min read"
author: "EgoistAI"
featured: false
tags: ["ai", "mcp", "tutorial", "claude", "api", "integration", "automation"]
sources:
  - name: "Anthropic MCP Documentation"
    url: "https://modelcontextprotocol.io/introduction"
  - name: "MCP Specification (GitHub)"
    url: "https://github.com/modelcontextprotocol/specification"
  - name: "Anthropic MCP Servers Repository"
    url: "https://github.com/modelcontextprotocol/servers"
---

## The Problem MCP Solves

You know the drill. You want Claude to help you debug a database issue, so you copy-paste the schema. Then the error log. Then the relevant code. Then you realize you forgot a table, so you paste that too. By the time you've assembled enough context, you've burned ten minutes and your chat window looks like a crime scene.

Model Context Protocol (MCP) kills this workflow entirely.

MCP is an open standard — created by Anthropic but not locked to Claude — that lets AI models connect directly to your data sources and tools. Instead of you being the middleman, shuttling text between your terminal and a chat window, the AI reaches out and grabs what it needs.

Think of it like USB for AI. Before USB, every peripheral needed its own proprietary connector. MCP does the same thing for AI integrations: one protocol, any tool.

## What MCP Actually Is (No Buzzwords)

MCP follows a client-server architecture. Here's what matters:

- **MCP Host**: The application you're using (Claude Desktop, Claude Code, or any MCP-compatible client)
- **MCP Client**: Lives inside the host, manages connections to servers
- **MCP Server**: A lightweight program that exposes specific capabilities — file access, database queries, API calls, whatever you build

The server exposes three types of things:

1. **Tools** — Functions the AI can call (like "run this SQL query" or "send a Slack message")
2. **Resources** — Data the AI can read (like file contents or database schemas)
3. **Prompts** — Pre-built prompt templates for common tasks

The server runs locally on your machine. Your data doesn't get routed through some third-party service. The AI model talks to the MCP client, which talks to the server, which talks to your stuff. Clean and simple.

## Prerequisites

Before we start, make sure you have:

- **Node.js 18+** — Most MCP servers are built in TypeScript. Run `node --version` to check.
- **Python 3.10+** — For Python-based servers. Run `python3 --version`.
- **Claude Desktop** or **Claude Code** — You need an MCP-compatible host. Claude Desktop is the GUI option, Claude Code is the CLI.
- **Basic terminal comfort** — You'll be editing JSON config files and running commands.

Got all that? Let's build.

## Step 1: Your First MCP Server (File System Access)

The fastest way to understand MCP is to give Claude access to your file system. Anthropic maintains an official filesystem server that does exactly this.

### Install It

```bash
npm install -g @modelcontextprotocol/server-filesystem
```

### Configure Claude Desktop

Open your Claude Desktop config file:

- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

Add this:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/Users/yourname/projects",
        "/Users/yourname/documents"
      ]
    }
  }
}
```

Replace the paths with directories you actually want Claude to access. This is important — MCP servers only get access to what you explicitly grant.

### Configure Claude Code

If you're using Claude Code (the CLI), it's even simpler. From your project directory:

```bash
claude mcp add filesystem -- npx -y @modelcontextprotocol/server-filesystem /path/to/your/project
```

Or edit `.claude/settings.json` in your project root:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "."
      ]
    }
  }
}
```

### Test It

Restart Claude Desktop (or your Claude Code session) and ask: "List all the files in my projects directory." If it works, Claude will use the filesystem tools to browse and read your files directly. No copy-pasting required.

## Step 2: Connect to a Database

File access is useful, but database access is where MCP gets genuinely powerful. Let's connect Claude to a PostgreSQL database.

### Install the Postgres Server

```bash
npm install -g @modelcontextprotocol/server-postgres
```

### Configure It

Add this to your `claude_desktop_config.json` (alongside your filesystem entry):

```json
{
  "mcpServers": {
    "filesystem": {
      "...": "your existing config"
    },
    "postgres": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-postgres",
        "postgresql://username:password@localhost:5432/your_database"
      ]
    }
  }
}
```

Now Claude can:

- Inspect your schema (`\dt`, `\d tablename` equivalents)
- Run read queries against your data
- Help you write and debug complex SQL
- Understand relationships between tables without you explaining them

### The Power Move

Try this prompt after connecting: *"Look at my database schema and suggest indexes I'm missing based on the table relationships and likely query patterns."*

Claude will pull the schema itself, analyze foreign keys and column types, and give you specific `CREATE INDEX` statements. That's the kind of thing that would take 20 minutes of manual context assembly without MCP.

## Step 3: API Integrations (Slack, GitHub, and More)

The MCP ecosystem already has servers for the tools you probably use daily.

### GitHub

```bash
npm install -g @modelcontextprotocol/server-github
```

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_your_token_here"
      }
    }
  }
}
```

With this configured, Claude can create issues, review PRs, search repositories, manage branches, and read code — all without you leaving the conversation.

Real use case: *"Look at the open PRs in my repo and summarize which ones have merge conflicts."* Claude calls the GitHub API, checks each PR, and gives you a rundown. Done in seconds.

### Slack

```bash
npm install -g @anthropic/mcp-server-slack
```

```json
{
  "mcpServers": {
    "slack": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-server-slack"],
      "env": {
        "SLACK_BOT_TOKEN": "xoxb-your-bot-token",
        "SLACK_TEAM_ID": "T0YOUR_TEAM"
      }
    }
  }
}
```

Now Claude can read channels, search message history, and post messages. Useful for things like: *"Summarize what the engineering team discussed in #dev today"* or *"Draft a release announcement for #general based on the latest GitHub release."*

### Combining Servers

This is where it gets wild. With multiple servers configured, Claude can chain operations across tools:

1. Read a GitHub issue
2. Check the relevant code in your filesystem
3. Query the database to understand the data model
4. Draft a fix and create a PR
5. Post a summary to Slack

All in one conversation. You describe what you want, and MCP handles the plumbing.

## Step 4: Build a Custom MCP Server

Pre-built servers are great, but the real power is building your own. Let's create a custom server that connects Claude to an internal REST API.

### TypeScript Example

First, set up the project:

```bash
mkdir my-api-server && cd my-api-server
npm init -y
npm install @modelcontextprotocol/sdk zod
npm install -D typescript @types/node
npx tsc --init
```

Now create `src/index.ts`:

```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const server = new McpServer({
  name: "internal-api",
  version: "1.0.0",
});

// Define a tool that fetches user data from your internal API
server.tool(
  "get_user",
  "Fetch user details from the internal API",
  {
    userId: z.string().describe("The user ID to look up"),
  },
  async ({ userId }) => {
    const response = await fetch(
      `https://internal-api.yourcompany.com/users/${userId}`,
      {
        headers: {
          Authorization: `Bearer ${process.env.API_TOKEN}`,
        },
      }
    );
    const user = await response.json();

    return {
      content: [
        {
          type: "text",
          text: JSON.stringify(user, null, 2),
        },
      ],
    };
  }
);

// Define a tool that searches your internal knowledge base
server.tool(
  "search_docs",
  "Search the internal documentation",
  {
    query: z.string().describe("Search query"),
    limit: z.number().optional().default(5).describe("Max results"),
  },
  async ({ query, limit }) => {
    const response = await fetch(
      `https://internal-api.yourcompany.com/docs/search?q=${encodeURIComponent(query)}&limit=${limit}`,
      {
        headers: {
          Authorization: `Bearer ${process.env.API_TOKEN}`,
        },
      }
    );
    const results = await response.json();

    return {
      content: [
        {
          type: "text",
          text: JSON.stringify(results, null, 2),
        },
      ],
    };
  }
);

// Connect via stdio transport
const transport = new StdioServerTransport();
await server.connect(transport);
```

Build and register it:

```bash
npx tsc
```

```json
{
  "mcpServers": {
    "internal-api": {
      "command": "node",
      "args": ["/absolute/path/to/my-api-server/dist/index.js"],
      "env": {
        "API_TOKEN": "your_api_token_here"
      }
    }
  }
}
```

### Python Example

Prefer Python? The MCP SDK has you covered.

```bash
pip install mcp[cli]
```

Create `server.py`:

```python
from mcp.server.fastmcp import FastMCP
import httpx

mcp = FastMCP("internal-api")

@mcp.tool()
async def get_user(user_id: str) -> str:
    """Fetch user details from the internal API."""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://internal-api.yourcompany.com/users/{user_id}",
            headers={"Authorization": f"Bearer {os.environ['API_TOKEN']}"},
        )
        return response.text

@mcp.tool()
async def search_docs(query: str, limit: int = 5) -> str:
    """Search the internal documentation."""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://internal-api.yourcompany.com/docs/search",
            params={"q": query, "limit": limit},
            headers={"Authorization": f"Bearer {os.environ['API_TOKEN']}"},
        )
        return response.text

if __name__ == "__main__":
    mcp.run(transport="stdio")
```

Register it:

```json
{
  "mcpServers": {
    "internal-api": {
      "command": "python3",
      "args": ["/absolute/path/to/server.py"],
      "env": {
        "API_TOKEN": "your_api_token_here"
      }
    }
  }
}
```

The Python SDK's `FastMCP` class handles all the protocol details. You just define functions with type hints and docstrings, and the SDK turns them into MCP tools automatically.

## Real-World Use Cases That Actually Matter

Here's where people are getting real value from MCP right now:

### DevOps Debugging

Connect Claude to your logs (filesystem server), your database (postgres server), and your monitoring API (custom server). When something breaks at 2 AM, ask Claude to correlate error spikes with recent deployments and database slow queries. It pulls from all three sources and gives you a diagnosis.

### Content Pipeline Automation

Connect Claude to your CMS API, image storage, and analytics database. Ask it to identify your top-performing content topics, draft new articles matching those patterns, and push them to your CMS as drafts. The entire pipeline runs through conversation.

### Customer Support Intelligence

Connect Claude to your support ticket system (custom server), your product database, and Slack. It can analyze ticket trends, identify recurring bugs, draft responses to common issues, and flag critical ones in your engineering Slack channel.

### Data Analysis on Demand

Connect Claude to your data warehouse. Instead of writing SQL, switching to your BI tool, and building dashboards, just ask: *"What's the month-over-month revenue trend for Q1, broken down by product line?"* Claude writes the query, runs it, and interprets the results.

## Common Pitfalls (and How to Avoid Them)

### 1. Forgetting to Restart

After changing your MCP config, you must restart Claude Desktop or your Claude Code session. The servers are initialized at startup. If you just saved the config and wonder why nothing works — restart.

### 2. Path Issues

MCP server commands need absolute paths. `~/projects` won't work in the JSON config on every platform. Use `/Users/yourname/projects` (macOS) or `C:\\Users\\yourname\\projects` (Windows) instead.

### 3. Permission Scope Creep

Don't give the filesystem server access to `/` or your entire home directory. Be specific. Grant access only to the directories the AI actually needs. This isn't just security — it also helps Claude focus on relevant files instead of getting lost in your node_modules.

### 4. Token/Credential Management

Never hardcode secrets directly in the config file if you share your dotfiles. Use environment variables or a secrets manager. The `env` field in MCP config is a good start, but for production setups, pull from your system keychain or a vault.

### 5. Server Crashes Silently

If an MCP server crashes, Claude just loses access to those tools — it doesn't throw an error in your face. If tools suddenly stop working, check the server logs:

- **Claude Desktop**: Look in `~/Library/Logs/Claude/` (macOS)
- **Claude Code**: Run with `--mcp-debug` flag for verbose output

### 6. Overloading with Servers

Each MCP server adds overhead and token usage (tool descriptions count against your context window). Don't connect 15 servers if you only need 3. Be deliberate about what you connect for each project.

## What's Next for MCP

MCP is still young but moving fast. The ecosystem of community-built servers is growing weekly — there are already servers for Google Drive, Notion, Linear, Jira, MongoDB, Redis, Docker, and dozens more on the [MCP servers repository](https://github.com/modelcontextprotocol/servers).

The bigger picture: MCP is shifting AI from a "smart text box" to an actual agent that can interact with your infrastructure. The models are ready. The protocol is here. The only bottleneck left is connecting everything — and that's what MCP servers are for.

If you build a custom server for your team's internal tools, you're not just making Claude more useful. You're building the interface layer between AI and your entire organization. That's the kind of infrastructure that compounds.

Start with one server. Get comfortable. Then connect everything.
