# MCP Task Manager — Connecting AI Agents with External Tools

A practical Python project demonstrating how to build an MCP (Model Context Protocol) server, connect an AI agent to it, and execute external tools through the MCP communication layer.

## 1. Project Overview

The **MCP Task Manager** demonstrates how AI applications can interact with external tools through the Model Context Protocol.

An AI model can understand natural-language instructions, but it needs access to external capabilities to perform actions such as creating tasks, retrieving information, and managing data.

MCP provides a standardized communication layer between AI applications and external services.

In this project, we build a Python MCP server that exposes task-management tools and connect an AI agent to the server through an MCP client.

### What This Project Demonstrates

- Understanding MCP and the problem it solves.
- Building a functional MCP server using Python.
- Exposing custom Python functions as MCP tools.
- Connecting an AI agent to an MCP server.
- Discovering and invoking tools through the MCP protocol.
- Executing a real tool call and receiving its result.

## 2. Problem Statement

Traditionally, connecting an AI application to different external services requires separate integrations.

For example, an AI application might need custom integration code to communicate with databases, file systems, APIs, and other applications.

As the number of external services increases, managing these integrations becomes more complicated.

MCP addresses this challenge by providing a standardized communication protocol that allows AI applications to discover and interact with external capabilities through MCP servers.

**Our Solution:**

We use MCP to build a task-management server that allows an AI agent to interact with task data without directly implementing each task operation inside the agent.

## 3. What Is MCP?

MCP stands for **Model Context Protocol**.

It is an open protocol introduced by Anthropic in November 2024 that standardizes how AI applications communicate with external tools, data sources, and services.

Think of MCP like USB-C:

- USB-C provides a common connection standard for compatible devices.
- MCP provides a common communication standard for AI applications and external services.

### Main Components

| Component | Responsibility |
|---|---|
| MCP Host | The main AI application managing the interaction. |
| MCP Client | Communicates with MCP servers. |
| MCP Server | Exposes tools and other capabilities to AI applications. |

### MCP Capabilities

- **Tools:** Allow AI applications to perform actions.
- **Resources:** Provide access to contextual information and data.
- **Prompts:** Provide reusable instruction templates.

## 4. Project Architecture

The project follows this communication flow:

```text
              USER
                |
                v
          AI APPLICATION
                |
                v
             AI AGENT
                |
                v
           MCP CLIENT
                |
                | MCP Protocol
                |
                v
           MCP SERVER
                |
                v
         TASK MANAGEMENT
                |
          +-----+------+
          |            |
          v            v
       Add Task     List Tasks
          |            |
          +-----+------+
                |
                v
          TOOL RESULTS
                |
                v
             AI AGENT
                |
                v
        FINAL RESPONSE
```

### How It Works

1. The user provides a natural-language instruction.
2. The AI agent interprets the request.
3. The agent identifies the appropriate MCP tool.
4. The MCP client communicates with the MCP server.
5. The MCP server executes the requested Python function.
6. The result is returned through the MCP client.
7. The AI agent uses the result to generate a response.

## 5. Features

The Task Manager MCP server provides the following functionality:

| Feature | Description | MCP Capability |
|---|---|---|
| Add Task | Create a new task. | Tool |
| List Tasks | Retrieve existing tasks. | Tool |
| Task Information | Access task-related information. | Resource (if implemented) |

The AI agent can interpret user instructions and use the available tools to perform task-management operations.

## 6. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| MCP Python SDK | Building MCP servers and clients |
| LLM | Understanding user instructions and selecting tools |
| AI Agent | Managing the reasoning and tool-calling workflow |
| SQLite (if implemented) | Persistent task storage |
| VS Code | Development environment |

## 7. Project Structure

```text
mcp-task-manager/
│
├── server.py             # MCP server and tool definitions
├── agent.py              # AI agent and MCP client integration
├── requirements.txt      # Project dependencies
├── .env.example          # Example environment configuration
├── .gitignore
└── README.md
```

## 8. Installation and Setup

### Prerequisites

- Python 3.11 or later
- VS Code
- pip or uv
- An LLM provider or locally running model, depending on the agent implementation

### Step 1: Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd mcp-task-manager
```

### Step 2: Create a Virtual Environment

```bash
python -m venv venv
```

Activate the environment.

**Windows:**

```powershell
.\venv\Scripts\Activate.ps1
```

**Linux / macOS:**

```bash
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

The project uses the official MCP Python SDK.

Official documentation:

https://py.sdk.modelcontextprotocol.io/

### Step 4: Configure Environment Variables

Create a `.env` file based on `.env.example` and configure the required LLM settings.

Never commit API keys or other secrets to GitHub.

## 9. Running the Project

### Start the MCP Server

Run the server using the command appropriate to its configured transport.

For a Streamable HTTP server, the official SDK CLI supports:

```bash
mcp run server.py --transport streamable-http
```

### Start the AI Agent

Open another terminal and run:

```bash
python agent.py
```

The AI agent connects to the MCP server through an MCP client and accesses the tools exposed by the server.

## 10. Demonstration: MCP Tool Calling

This section demonstrates the core functionality of the project.

## 10. Demonstration: MCP Tool Calling

This section demonstrates the core functionality of the project using actual terminal output from the AI agent.

**Terminal Output:**
```text
--- User Query: Add a task called Learn Model Context Protocol. ---
-> Agent decided to call MCP tool: add_task
-> MCP Server Response:
Task added successfully:
Learn Model Context Protocol

-> Final Answer:
Task added successfully: Learn Model Context Protocol. If you need any assistance with this task or have further instructions, feel free to let me know!

--- User Query: Show me all my tasks. ---
-> Agent decided to call MCP tool: list_tasks
-> MCP Server Response:
Your tasks:

1. Learn Model Context Protocol
2. Build a Python MCP Server

-> Final Answer:
Here are your tasks:

1. Learn Model Context Protocol
2. Build a Python MCP Server

If you need any assistance with these tasks or have more tasks to add, feel free to let me know!

### Example 1: Create a Task

**User instruction:**

```text
Add a task called Learn Model Context Protocol.
```

**Expected execution flow:**

1. The AI agent understands the instruction.
2. The agent selects the `add_task` tool.
3. The MCP client sends a tool-call request.
4. The MCP server executes the tool.
5. The server returns the execution result.

**Example tool arguments:**

```json
{
  "task": "Learn Model Context Protocol"
}
```

**Example result:**

```text
Task added successfully:
Learn Model Context Protocol
```

### Example 2: Retrieve Tasks

**User instruction:**

```text
Show me all my tasks.
```

The AI agent selects the `list_tasks` tool.

The MCP server retrieves the task information and returns it to the AI agent.

**Example result:**

```text
Your tasks:

1. Learn Model Context Protocol
2. Build a Python MCP Server
3. Understand MCP Clients
```

*Note: These are illustrative demonstration outputs. Replace them with actual output from your running application.*

## 11. Why Use MCP Instead of Direct Integration?

Without MCP, an AI application may need separate custom integration logic for every external service.

With MCP, compatible AI applications can communicate with different MCP servers using a standardized protocol.

Benefits include:

- Standardized communication.
- Reusable integrations.
- Separation of AI logic and external services.
- Easier tool discovery.
- Better integration flexibility.
- Support for multiple AI applications and MCP servers.

**Important:** MCP does not replace REST APIs. An MCP server can use existing APIs internally while exposing capabilities through the MCP protocol.

## 12. Key Learnings

Through this project, the following concepts can be understood practically:

1. How MCP standardizes communication between AI applications and external services.
2. The responsibilities of MCP Hosts, Clients, and Servers.
3. How to expose Python functions as MCP tools.
4. How an AI agent discovers and selects available tools.
5. How MCP clients execute tool calls.
6. How external tool results are returned to an AI agent.
7. How AI agents can interact with external systems through MCP.

## 13. Future Improvements

Possible extensions include:

- Add task-update and task-deletion tools.
- Integrate PostgreSQL for persistent storage.
- Expose task information through MCP resources.
- Add task priorities and deadlines.
- Implement authentication and authorization.
- Connect additional MCP servers.
- Extend the workflow using LangGraph.

## 14. References

- [Official MCP Documentation](https://modelcontextprotocol.io/docs/getting-started/intro)
- [MCP Architecture](https://modelcontextprotocol.io/docs/learn/architecture)
- [Official Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [Python SDK Documentation](https://py.sdk.modelcontextprotocol.io/)

---

**Project:** MCP Task Manager

**Language:** Python

**Protocol:** Model Context Protocol (MCP)

**Purpose:** Demonstrating how AI agents connect to external tools and execute operations through MCP.