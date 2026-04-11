from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from resume_builder.utils import get_ollama_model
from langchain.tools import tool
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langgraph.checkpoint.memory import InMemorySaver

async def get_dkdkg_client_tools():
    print('starting duckduckgo mcp client')
    client = MultiServerMCPClient(
        {
            "dkdkg_web_search": {
                "transport": "stdio",
                "command": "uvx",
                "args": ["duckduckgo-mcp-server"]
            }
        }
    )

    tools = await client.get_tools()
    return tools

@tool(name_or_callable="duckduckgo_web_search")
async def get_dkdkg_agent(url: str, section_required: str):
    """
    Helpful agent which have access to duckduckgo mcp
    This agent will be very help for web search
    After fetching llm will summarize/extend mentioned section_required

    Args:
        url (str): str
        section_required (str): str

    Returns:
        _type_: str
    """
    model = get_ollama_model()
    tools = await get_dkdkg_client_tools()
    interrupt_on = {tool.name : True for tool in tools}
    hitl_middleware = HumanInTheLoopMiddleware(
        interrupt_on=interrupt_on
    )

    agent = create_agent(
        model=model,
        tools = tools,
        middleware=[hitl_middleware],
        checkpointer=InMemorySaver()
    )

    query = {"query": f"Extract {section_required} from this {url}"}
    response = await agent.ainvoke(query)
    return response
