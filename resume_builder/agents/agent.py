from langchain.agents import create_agent
from resume_builder.tools import read_local_file
from resume_builder.utils import get_ollama_model, MemoryProvider
from langchain.agents.middleware import HumanInTheLoopMiddleware
from resume_builder.tools import (
    get_file_management_toolkit,
    read_local_pdf_file,
    get_proper_interrupt,
)


def get_general_agent():
    model = get_ollama_model()

    agent = create_agent(
        model=model,
        tools=[read_local_file],
    )
    return agent


def get_file_system_explorer_agent():
    model = get_ollama_model()
    tools = get_file_management_toolkit()
    tools.append(read_local_pdf_file)
    interrupt_on = get_proper_interrupt(tools)

    hitl_middleware = HumanInTheLoopMiddleware(interrupt_on=interrupt_on)

    agent = create_agent(
        model=model,
        tools=tools,
        middleware=[hitl_middleware],
        checkpointer=MemoryProvider(),
    )
    return agent
