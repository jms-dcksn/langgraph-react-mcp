# app/agent.py
import asyncio
from langchain_openai import ChatOpenAI
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent

from app.utils import parse_agent_response

# Define your local LLM's API endpoint
local_llm = ChatOpenAI(
    model="llama3.2:3b",  # Replace with your model's name if different
    base_url="http://localhost:11434/v1"
)

async def stream_agent(message: str):
    async with MultiServerMCPClient(
        {
            "zapier": {
                "url": "https://actions.zapier.com/mcp/sk-ak-klURxXRKWKamKGQqadYx74muv5/sse",
                "transport": "sse",
            }
        }
    ) as client:
        agent = create_react_agent(
            #"anthropic:claude-3-7-sonnet-latest",
            local_llm,
            client.get_tools()
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
                    # for part in ai_chunk.content:
                    #     if isinstance(part, dict) and "text" in part:
                    #         full_message += part["text"]
                    #         yield full_message 
                    full_message += ai_chunk.content
                    yield full_message
                    #yield ai_chunk.content
                # Optionally, handle the final message for tool info
            elif chunk.get("event") == "on_chat_model_end":
                data = chunk.get("data", {})
                ai_message = data.get("output")
                if hasattr(ai_message, "content") and ai_message.content:
                    yield ai_message.content  # This is the final, full message
                # Add more cases as needed for your agent's output format