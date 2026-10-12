# Hello MCP

## A Beginner's Guide to Building Your First Model Context Protocol (MCP) Application

## Introduction

Welcome to this tutorial.

If you're new to the Model Context Protocol (MCP), this project is designed specifically for you.

Most MCP tutorials focus on building useful tools as quickly as possible. While that approach is great for experienced developers, it often skips the most important question:

> **How does MCP actually work?**

This tutorial takes a different approach.

Instead of building a complex application, we'll build the smallest possible MCP project and use it to understand the complete communication workflow between an MCP client and an MCP server.

By the end of this tutorial, you won't just know how to run an MCP application—you'll understand what happens internally every time an AI application communicates with an MCP server.

---

# Learning Objectives

After completing this tutorial, you should be able to:

- Explain what the Model Context Protocol (MCP) is.
- Understand the difference between an MCP Client and an MCP Server.
- Create an MCP server using the Python SDK.
- Register tools that can be discovered by clients.
- Build an MCP client that connects to the server.
- Discover available tools dynamically.
- Invoke tools through the MCP protocol.
- Understand how the client and server communicate using the Standard Input/Standard Output (stdio) transport.
- Recognize common mistakes when developing MCP applications.

This project intentionally keeps the implementation simple so that the focus remains on understanding the protocol itself.

---

# What You'll Build

During this tutorial, you'll build a complete MCP application consisting of two separate programs.

The first program is an **MCP Server**.

The server exposes one or more tools that other applications can discover and execute.

The second program is an **MCP Client**.

The client starts the server, establishes communication, discovers the available tools, invokes a tool, and displays the result.

The completed architecture looks like this:

```text
                   User
                     │
                     ▼
               python client.py
                     │
                     ▼
              MCP Client
                     │
             Model Context Protocol
                     │
                     ▼
              MCP Server
                     │
                     ▼
             Registered Tool
              (hello(name))
                     │
                     ▼
             Hello Engineer!
```

Although this project contains only a single greeting tool, it demonstrates the exact communication pattern used by much larger MCP servers.

Whether an MCP server exposes one tool or hundreds of tools, the workflow remains the same.

---

# Prerequisites

Before starting this tutorial, you should have:

- Basic knowledge of Python
- Python 3.14 or later installed
- Git installed
- A GitHub account
- GitHub Codespaces or Visual Studio Code

No prior MCP knowledge is required.

---

# Project Structure

After completing this tutorial, your project structure should look similar to the following:

```text
hello-mcp/
│
├── server.py
├── client.py
├── inspect_server.py
├── server_ping_google.py
├── client_ping_google.py
├── requirements.txt
├── README.md
└── .venv/
```

Each file has a specific purpose.

| File | Purpose |
|------|---------|
| `server.py` | Creates an MCP server and registers the `hello` tool. |
| `client.py` | Starts the server, initializes an MCP session, lists available tools, and invokes the `hello` tool. |
| `inspect_server.py` | Displays the tools registered with the server without starting a client. |
| `server_ping_google.py` | Demonstrates a more practical MCP server that checks whether Google is reachable. |
| `client_ping_google.py` | Connects to the Google Ping server and invokes the `ping_google` tool. |
| `requirements.txt` | Lists all Python dependencies required by the project. |

---

# Setting Up the Development Environment

This tutorial uses **GitHub Codespaces**, but the same commands work on Linux, macOS, or Windows (using PowerShell equivalents where necessary).

### Verify Python Installation

First, verify that Python is installed.

```bash
python --version
python3 --version
```

You should see output similar to:

```text
Python 3.14.x
```

---

### Create a Virtual Environment

Create a new virtual environment inside the project directory.

```bash
python -m venv .venv
```

Activate the environment.

On Linux or GitHub Codespaces:

```bash
source .venv/bin/activate
```

After activation, your terminal prompt should display:

```text
(.venv)
```

Using a virtual environment ensures that project dependencies remain isolated from other Python projects on your system.

---

### Install the MCP SDK

Install the MCP SDK and command-line tools.

```bash
pip install "mcp[cli]"
```

This command installs the MCP SDK together with its required dependencies.

---

### Save the Project Dependencies

Once the installation completes, generate a requirements file.

```bash
pip freeze > requirements.txt
```

This file allows anyone cloning the repository to recreate the same development environment by running:

```bash
pip install -r requirements.txt
```

Using a requirements file is considered a best practice because it keeps dependency versions consistent across different development environments.

---

At this point, the development environment is fully configured, and you're ready to build your first MCP server.

# Building Your First MCP Server

Now that the development environment is ready, it's time to build the server.

An **MCP Server** is responsible for exposing tools that other applications can discover and execute.

Think of it as a service that publishes capabilities.

Instead of writing code that directly calls Python functions, an MCP client communicates with the server using the Model Context Protocol.

The server receives requests, executes the appropriate tool, and returns the result.

Our server is intentionally simple so that we can focus on understanding the workflow.

---

## Creating the Server

The first step is creating an instance of `MCPServer`.

```python
from mcp.server import MCPServer

mcp = MCPServer("Hello MCP")
```

The string `"Hello MCP"` is the name of the server.

Clients can retrieve this information during the initialization process.

Although this project only creates a single server, an organization could build multiple MCP servers for different purposes.

For example:

- Database Server
- Filesystem Server
- Git Server
- Weather Server
- Internal Company Tools

Each server would expose a different collection of tools.

---

## Registering a Tool

Now let's create our first tool.

```python
@mcp.tool()
def hello(name: str) -> str:
    """
    Return a greeting.
    """
    return f"Hello {name}!"
```

This decorator is one of the most important concepts in the MCP SDK.

When Python loads this file, the SDK automatically registers the function as an MCP tool.

Without writing any additional code, the SDK extracts information such as:

- Tool name
- Function parameters
- Parameter types
- Return type
- Description from the docstring

Later, when a client asks the server for a list of available tools, this information is returned automatically.

In other words, you don't manually create a JSON description of the tool—the SDK generates it for you.

---

## Starting the Server

Finally, the server is started using:

```python
if __name__ == "__main__":
    mcp.run()
```

This tells the SDK to start listening for incoming MCP requests.

At this point, the server is ready to communicate with any compatible MCP client.

---

## Why Does the Server Appear to Do Nothing?

One of the first things beginners notice is that running:

```bash
python server.py
```

doesn't display any output.

It simply waits.

This is expected behavior.

Unlike a traditional command-line application, an MCP server is **not designed for direct interaction with a user**.

Instead, it waits for another application to connect and send protocol messages.

You can think of the server as a receptionist waiting for phone calls.

Until a client contacts it, there is nothing to do.

---

## How the Server Fits into the MCP Workflow

The server is only one half of the application.

Its responsibility is to expose tools.

It does **not** decide which tool to execute.

That decision is made by the client.

The interaction looks like this:

```text
Client
   │
   │ Request: List available tools
   ▼
Server
   │
   ▼
hello
```

Later:

```text
Client
   │
   │ Request: Execute hello()
   ▼
Server
   │
   ▼
Hello Engineer!
```

Notice that the client never imports or directly calls the `hello()` function.

Instead, all communication happens through the MCP protocol.

This separation is one of the key design principles of MCP.

---

# Building the MCP Client

Now that the server is ready, we need a program capable of communicating with it.

This is the role of the **MCP Client**.

The client is responsible for:

1. Starting the MCP server.
2. Establishing communication.
3. Initializing an MCP session.
4. Discovering available tools.
5. Calling tools.
6. Receiving and displaying results.

Unlike the server, the client is an application that users interact with directly.

---

## Configuring the Server Process

The first thing the client needs to know is **how to start the server**.

This is done using `StdioServerParameters`.

```python
server = StdioServerParameters(
    command="python",
    args=["server.py"],
)
```

This configuration tells the client:

> "Whenever you need the server, launch it by executing `python server.py`."

Notice that we never start the server manually.

The client starts the server automatically whenever it needs it.

---

## Creating the Transport

Next, the client establishes communication using the Standard Input/Standard Output (stdio) transport.

```python
async with stdio_client(server) as (read_stream, write_stream):
```

The transport creates two communication channels.

```text
Client
   │
   │ write_stream
   ├────────────────────► Server

Client
   │
   │ read_stream
   ◄───────────────────── Server
```

Everything exchanged between the client and server travels through these two streams.

The client writes protocol messages to the server.

The server processes the request and sends a response back through the read stream.

---

## Creating a Client Session

Once the transport is established, we create an MCP session.

```python
async with ClientSession(read_stream, write_stream) as session:
```

The session provides a high-level interface for interacting with the server.

Instead of manually constructing protocol messages, we can simply call methods such as:

- `initialize()`
- `list_tools()`
- `call_tool()`

Internally, these methods generate the appropriate MCP requests and handle the responses automatically.

---

## Initializing the Session

Before any tools can be used, the client and server perform an initialization handshake.

```python
await session.initialize()
```

During initialization, both sides exchange information such as supported protocol capabilities and server metadata.

Only after initialization completes can the client begin discovering and invoking tools.

You can think of this as the equivalent of establishing a connection before beginning a conversation.

---

## Discovering Available Tools

One of MCP's most useful features is that clients do not need prior knowledge of the available tools.

Instead, they can ask the server to provide a list.

```python
tools = await session.list_tools()
```

The server responds with metadata describing every registered tool.

The client then prints each tool name.

```python
for tool in tools.tools:
    print(tool.name)
```

This means the client can adapt automatically if new tools are added to the server in the future without requiring any changes to the client itself.

---

## Invoking a Tool

Finally, the client calls the `hello` tool.

```python
result = await session.call_tool(
    "hello",
    {"name": "Engineer"},
)
```

The first argument is the tool name.

The second argument is a dictionary containing the tool's input parameters.

The server executes the function and returns the response.

The client reads the response and prints:

```text
Hello Engineer!
```

Although it appears as though the client is calling a Python function directly, that is not what happens.

Instead, the client sends an MCP request to the server.

The server receives the request, executes the registered tool, and sends the result back through the protocol.

This request-response cycle forms the foundation of every MCP application.

# Inspecting Registered Tools

During development, it is often useful to verify that the server has correctly registered all of its tools before connecting a client.

To help with this, this project includes a small utility called `inspect_server.py`.

Run it using:

```bash
python inspect_server.py
```

Expected output:

```text
Server Name: Hello MCP

Registered tools:
- hello
```

Unlike `client.py`, this script **does not start an MCP session**.

Instead, it imports the server, accesses the `MCPServer` instance, and asks it for the list of registered tools. This allows you to quickly confirm that your server configuration is correct without creating a client connection.

This utility is especially helpful as your server grows and begins exposing multiple tools.

---

# Understanding Tool Registration

One question that many beginners ask is:

> "How does the server know about my `hello()` function?"

The answer is the `@mcp.tool()` decorator.

When Python imports `server.py`, every decorated function is automatically registered with the server.

The registration process stores metadata about each tool, including:

- Tool name
- Input parameters
- Parameter types
- Return type
- Description (if a docstring is provided)

Conceptually, the process looks like this:

```text
Python imports server.py
           │
           ▼
Decorator executes
           │
           ▼
Tool metadata is created
           │
           ▼
Tool is registered with MCPServer
           │
           ▼
Client can now discover it
```

Because of this automatic registration, you never need to manually maintain a list of available tools.

As long as a function is decorated with `@mcp.tool()`, it becomes available to every connected client.

---

# Understanding the MCP Communication Workflow

Now that we've seen both the server and the client, let's examine the complete lifecycle of an MCP request.

Suppose we execute:

```bash
python client.py
```

Internally, the following sequence of events occurs.

## Step 1 — The Client Starts

Execution begins in `client.py`.

The client creates the server configuration using `StdioServerParameters`.

```text
Client Started
       │
       ▼
Create Server Parameters
```

---

## Step 2 — The Server Process Starts

The client launches the server process automatically.

You do **not** need to open another terminal or manually execute:

```bash
python server.py
```

The MCP SDK handles this for you.

```text
Client
   │
   │ Launch server.py
   ▼
Server Process
```

---

## Step 3 — Communication Channels Are Created

Next, the stdio transport creates two communication channels.

```text
Client stdout ─────────────► Server stdin

Server stdout ─────────────► Client stdin
```

Every MCP request and response travels through these streams.

No HTTP server is required.

No REST API is involved.

Everything happens over the operating system's standard input and output streams.

---

## Step 4 — Session Initialization

Before any tool can be called, the client initializes the session.

```python
await session.initialize()
```

During initialization, the client and server exchange information such as:

- Server name
- Supported protocol version
- Supported capabilities

Only after this handshake completes can requests be exchanged.

Conceptually:

```text
Client
   │ initialize()
   ▼
Server

Server
   │ Initialization Complete
   ▼
Client
```

---

## Step 5 — Tool Discovery

The client asks:

> "What tools do you provide?"

Internally, this is performed by:

```python
await session.list_tools()
```

The server responds with metadata describing every registered tool.

Example:

```text
hello
```

Notice that the client never imports `server.py`.

Instead, it discovers tools dynamically through the MCP protocol.

This makes MCP applications highly extensible.

If tomorrow you register ten additional tools, the client can discover them without changing a single line of client code.

---

## Step 6 — Tool Invocation

The client now sends a request to execute a tool.

```python
await session.call_tool(
    "hello",
    {"name": "Engineer"}
)
```

The server performs three actions:

1. Finds the registered tool.
2. Executes the corresponding Python function.
3. Returns the result.

Conceptually:

```text
Client
   │
   │ call_tool("hello")
   ▼
Server
   │
   ▼
hello("Engineer")
   │
   ▼
"Hello Engineer!"
   │
   ▼
Client
```

The client then displays the returned value to the user.

---

# A More Practical Example

Greeting a user is useful for learning the protocol, but real MCP servers typically expose tools that perform meaningful work.

To demonstrate this, the project also includes:

```text
server_ping_google.py
client_ping_google.py
```

These files implement another MCP server that exposes a `ping_google` tool.

Instead of returning a greeting, this tool attempts to contact Google and reports whether the request succeeds.

The workflow is identical to the greeting example.

```text
Client
      │
      ▼
Start Google Server
      │
      ▼
Initialize Session
      │
      ▼
Discover ping_google Tool
      │
      ▼
Execute Tool
      │
      ▼
Receive Status
```

The important lesson here is that **the workflow never changes**.

Whether the server exposes:

- a greeting,
- a calculator,
- a database query,
- a filesystem browser,
- or a weather service,

the client always performs the same sequence:

1. Connect
2. Initialize
3. Discover
4. Invoke
5. Receive the response

Only the implementation of the tool changes.

---

# Common Mistakes

While building this project, several common issues appeared. Understanding them will save you a significant amount of debugging time.

## Printing to stdout

One of the easiest mistakes to make is adding a debugging statement such as:

```python
print("Starting server...")
```

This breaks the MCP protocol.

Why?

Because the server communicates with the client through **stdout**.

The client expects every line written to stdout to be valid MCP protocol data.

If ordinary text is written to stdout, the client attempts to interpret it as a protocol message and fails.

If you need logging, write to **stderr** instead.

```python
import sys

print("Starting server...", file=sys.stderr)
```

Alternatively, configure Python's `logging` module to use `stderr`.

---

## The Server Appears to Hang

Running:

```bash
python server.py
```

may appear to do nothing.

This is expected.

The server is waiting for a client connection.

It is not frozen.

---

## Forgetting to Initialize the Session

Calling:

```python
await session.call_tool(...)
```

before:

```python
await session.initialize()
```

will result in errors because the client and server have not completed the initialization handshake.

Always initialize the session before sending requests.

---

## Forgetting to Await Asynchronous Functions

Most client operations are asynchronous.

For example:

```python
await session.list_tools()
```

If `await` is omitted, Python returns a coroutine object instead of executing the request.

Whenever you see a message mentioning a **coroutine was never awaited**, it usually indicates that an asynchronous function was called without `await`.

---

# Where to Go From Here

This project intentionally remains small.

The goal is not to build a feature-rich application, but to develop a solid understanding of the Model Context Protocol.

Once you're comfortable with the concepts introduced here, consider extending the project with additional tools such as:

- A calculator that performs arithmetic operations.
- A filesystem server that reads local files.
- A SQLite server capable of executing SQL queries.
- A weather server that calls a public API.
- A Git server that exposes repository information.

Each of these projects follows the exact same architecture introduced in this tutorial.

Only the tools change—the client-server communication model remains the same.

---

# Conclusion

Congratulations!

You have built and explored a complete Model Context Protocol application from scratch.

Although the example project is intentionally simple, it demonstrates every core component of an MCP application:

- Creating an MCP server.
- Registering tools.
- Starting a client.
- Establishing communication using stdio.
- Initializing an MCP session.
- Discovering available tools.
- Invoking tools through the protocol.
- Receiving structured responses.

These concepts form the foundation of every MCP application, from small local utilities to production systems integrated with AI assistants.

With this foundation in place, you'll be well prepared to build more advanced MCP servers and understand how modern AI applications extend their capabilities through the Model Context Protocol.

# Frequently Asked Questions

## Why doesn't `python server.py` produce any output?

This is expected behavior.

An MCP server is not an interactive command-line application. It waits for an MCP client to connect and send requests.

Once a client establishes a connection, the server begins processing protocol messages.

---

## Why does the client start the server automatically?

The client creates a `StdioServerParameters` object that describes how to launch the server.

```python
server = StdioServerParameters(
    command="python",
    args=["server.py"],
)
```

When the client executes, it starts the server process automatically.

There is no need to manually execute `python server.py` in another terminal.

---

## Why does the project use asynchronous programming?

The MCP SDK is built on asynchronous communication.

Operations such as:

- Initializing a session
- Listing tools
- Calling tools
- Reading resources

all involve waiting for responses from another process.

Using Python's `async` and `await` allows the client to continue handling other work while waiting for those responses.

Although asynchronous programming may seem unnecessary in a small project, it becomes essential when an MCP server exposes many tools or performs network and database operations.

---

## Why is `stdout` reserved?

The stdio transport uses:

- `stdin` for incoming protocol messages.
- `stdout` for outgoing protocol messages.

Because of this, any ordinary text printed to `stdout` corrupts the communication channel.

For debugging, always use:

```python
import sys

print("Debug message", file=sys.stderr)
```

or configure the Python `logging` module to write to `stderr`.

---

## Can one server expose multiple tools?

Yes.

A single MCP server can expose as many tools as required.

For example:

```python
@mcp.tool()
def add(a: int, b: int):
    return a + b


@mcp.tool()
def subtract(a: int, b: int):
    return a - b


@mcp.tool()
def multiply(a: int, b: int):
    return a * b
```

The client will automatically discover every registered tool during the `list_tools()` request.

---

## Can multiple clients connect to the same server?

Yes.

Depending on the transport being used, multiple clients may communicate with the same server.

This project uses the **stdio** transport, which launches a dedicated server process for each client.

Other transports, such as Server-Sent Events (SSE) or Streamable HTTP, are designed for longer-running servers that can handle multiple client connections.

---

# Next Projects

This repository focuses on understanding the core workflow of the Model Context Protocol.

Once you are comfortable with these concepts, try extending the project by implementing additional tools.

Some good beginner projects include:

### Calculator MCP Server

Expose tools such as:

- add
- subtract
- multiply
- divide

This introduces multiple tools and parameter validation.

---

### Filesystem MCP Server

Create tools that:

- List files
- Read files
- Search directories

This introduces file handling and resource access.

---

### SQLite MCP Server

Expose tools such as:

- Execute SQL queries
- List database tables
- Describe table schemas

This introduces database integration while keeping the project self-contained.

---

### Weather MCP Server

Connect to a public weather API and expose tools that retrieve current weather conditions.

This introduces working with external APIs.

---

### Git MCP Server

Expose Git operations such as:

- Current branch
- Commit history
- Repository status

This introduces interaction with external applications.

---

# Repository Contents

```text
hello-mcp/
│
├── server.py
│   └── Defines the Hello MCP server and registers the greeting tool.
│
├── client.py
│   └── Starts the server, initializes an MCP session, discovers tools,
│       invokes the hello tool, and prints the response.
│
├── inspect_server.py
│   └── Lists the tools currently registered with the server.
│
├── server_ping_google.py
│   └── Demonstrates an MCP server exposing a network utility.
│
├── client_ping_google.py
│   └── Demonstrates invoking the ping_google tool.
│
├── requirements.txt
│   └── Python dependencies.
│
└── README.md
    └── Complete tutorial explaining the project.
```

---

# Key Takeaways

After working through this tutorial, you should understand the complete lifecycle of a basic MCP application.

1. Build an MCP server.
2. Register one or more tools.
3. Start the server through the client.
4. Establish communication using the stdio transport.
5. Initialize the MCP session.
6. Discover available tools dynamically.
7. Invoke a tool by name.
8. Receive a structured response from the server.

Although the example application is intentionally simple, these same concepts apply to much larger MCP servers used by AI assistants and developer tools.

Understanding this workflow provides a strong foundation for building more advanced MCP applications.

---

# References

- Model Context Protocol (MCP) Specification
- MCP Python SDK Documentation
- GitHub Codespaces Documentation
- Python `asyncio` Documentation

---

# License

This project is intended for educational purposes.

You are welcome to use, modify, and extend the code to build your own MCP servers and clients.

---

# Acknowledgements

This project was created as a step-by-step learning resource for developers who want to understand the fundamentals of the Model Context Protocol before moving on to larger, production-ready MCP applications.
