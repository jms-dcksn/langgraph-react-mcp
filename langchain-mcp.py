import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent

async def run_agent():
    async with MultiServerMCPClient(
        {
        "zapier": {
            # Ensure your start your weather server on port 8000
            "url": "https://actions.zapier.com/mcp/sk-ak-klURxXRKWKamKGQqadYx74muv5/sse",
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
