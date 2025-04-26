import asyncio
from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent

import os

load_dotenv()  # take environment variables from .env.

zapier_url = os.getenv("ZAPIER_URL")

async def run_agent():
    async with MultiServerMCPClient(
        {
        "zapier": {
            # Ensure your start your weather server on port 8000
            "url": zapier_url,
            "transport": "sse",
        }
    }
) as client:
        agent = create_react_agent(
        "anthropic:claude-3-7-sonnet-latest",
        client.get_tools()
        )
        response = await agent.ainvoke({
            "messages": "Send a chuck norris joke as a slack message to jms.dcksn88@gmail.com"})        
        print(response)

async def main():
    await run_agent()
# Run the main function using asyncio.run
if __name__ == "__main__":
    asyncio.run(main())
