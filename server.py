import sqlite3
from mcp.server import MCPServer

# Initialize MCP Server
mcp = MCPServer("TaskManager")

# Setup SQLite database
def setup_db():
    conn = sqlite3.connect(":memory:", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE tasks (id INTEGER PRIMARY KEY, task TEXT)")
    # Pre-populate with example tasks from README
    cursor.execute("INSERT INTO tasks (task) VALUES ('Learn Model Context Protocol')")
    cursor.execute("INSERT INTO tasks (task) VALUES ('Build a Python MCP Server')")
    conn.commit()
    return conn

db_conn = setup_db()

@mcp.tool()
def add_task(task: str) -> str:
    """Create a new task."""
    cursor = db_conn.cursor()
    cursor.execute("INSERT INTO tasks (task) VALUES (?)", (task,))
    db_conn.commit()
    return f"Task added successfully:\n{task}"

@mcp.tool()
def list_tasks() -> str:
    """Retrieve existing tasks."""
    cursor = db_conn.cursor()
    cursor.execute("SELECT id, task FROM tasks")
    rows = cursor.fetchall()
    
    if not rows:
        return "No tasks found."
        
    result = "Your tasks:\n\n"
    for row in rows:
        result += f"{row[0]}. {row[1]}\n"
    return result.strip()

if __name__ == "__main__":
    mcp.run()