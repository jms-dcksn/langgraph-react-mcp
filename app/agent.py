# app/agent.py
import asyncio
from langchain_openai import ChatOpenAI
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent

from dotenv import load_dotenv
import os

load_dotenv()  # take environment variables from .env.

zapier_url = os.getenv("ZAPIER_URL")
print(zapier_url)

# Define your local LLM's API endpoint
local_llm = ChatOpenAI(
    model="gpt-4o-mini",  # Replace with your model's name if different
    #base_url="http://localhost:11434/v1"
)

async def stream_agent(message: str):
    client = MultiServerMCPClient({
            "jd-test": {
                "url": zapier_url,
                "transport": "streamable_http",
            },
            "math": {
                "command": "python",
                "args": ["/Users/jamesdickson/Projects/langchain-mcp/app/math_server.py"],
                "transport": "stdio",
            }
        })
    tools = await client.get_tools()
    agent = create_react_agent(
            #"anthropic:claude-3-7-sonnet-latest",
            local_llm,
            tools
        )
    full_message = ""
        # This assumes your agent supports astream or similar
    async for chunk in agent.astream_events({"messages": message}):
            print("DEBUG: chunk =", chunk)
            # Only process 'on_chat_model_stream' events
            if chunk.get("event") == "on_chat_model_stream":
                data = chunk.get("data", {})
                ai_chunk = data.get("chunk")
                if hasattr(ai_chunk, "content") and ai_chunk.content:
                    full_message += ai_chunk.content
                    yield full_message
                # Optionally, handle the final message for tool info
            elif chunk.get("event") == "on_chat_model_end":
                data = chunk.get("data", {})
                ai_message = data.get("output")
                if hasattr(ai_message, "content") and ai_message.content:
                    yield ai_message.content  # This is the final, full message
                # Add more cases as needed for your agent's output format