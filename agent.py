import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from openai import OpenAI

# Point OpenAI client to local Ollama
llm = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
MODEL_NAME = "qwen2.5"

async def run_agent(user_query: str):
    server_params = StdioServerParameters(command="python", args=["server.py"])

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # Get tools
            tools_response = await session.list_tools()
            openai_tools = [{
                "type": "function",
                "function": {
                    "name": t.name,
                    "description": t.description,
                    "parameters": t.input_schema,
                }
            } for t in tools_response.tools]

            print(f"\n--- User Query: {user_query} ---")
            messages = [{"role": "user", "content": user_query}]

            # First LLM Call
            response = llm.chat.completions.create(
                model=MODEL_NAME, messages=messages, tools=openai_tools
            )
            response_message = response.choices[0].message
            messages.append(response_message)

            # Tool Execution
            if response_message.tool_calls:
                for tool_call in response_message.tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)
                    
                    print(f"-> Agent decided to call MCP tool: {function_name}")
                    result = await session.call_tool(function_name, arguments=function_args)
                    tool_output = result.content[0].text
                    
                    print(f"-> MCP Server Response:\n{tool_output}\n")

                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": tool_output,
                    })

                # Final LLM Call
                final_response = llm.chat.completions.create(
                    model=MODEL_NAME, messages=messages
                )
                print(f"-> Final Answer:\n{final_response.choices[0].message.content}")
            else:
                print("No tool call was made.")

async def main():
    # Run Example 1
    await run_agent("Add a task called Learn Model Context Protocol.")
    # Run Example 2
    await run_agent("Show me all my tasks.")

if __name__ == "__main__":
    asyncio.run(main())