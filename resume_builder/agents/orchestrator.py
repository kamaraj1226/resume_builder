from langchain.agents.middleware import HumanInTheLoopMiddleware
from langchain.agents import create_agent

from resume_builder.utils import get_ollama_model, MemoryProvider
from resume_builder.agents.agent_as_tools import (
    personalize_latex_with_jd_tool,
    pdf_to_latex_agent_tool,
    get_user_input_tool,
    read_local_pdf_file,
)
from resume_builder.tools import get_proper_interrupt, get_file_management_toolkit
from resume_builder.system_prompts import ORCHESTRATOR


def orchestrator_agent():
    model = get_ollama_model()
    file_system_toolkit = get_file_management_toolkit()
    tools = [
        personalize_latex_with_jd_tool,
        pdf_to_latex_agent_tool,
        get_user_input_tool,
        read_local_pdf_file,
    ]
    tools.extend(file_system_toolkit)
    interrupt_on = get_proper_interrupt(tools=tools)

    hitl_middleware = HumanInTheLoopMiddleware(interrupt_on=interrupt_on)

    agent = create_agent(
        model=model,
        tools=tools,
        middleware=[hitl_middleware],
        checkpointer=MemoryProvider().checkpointer,
        system_prompt=ORCHESTRATOR,
    )

    return agent
