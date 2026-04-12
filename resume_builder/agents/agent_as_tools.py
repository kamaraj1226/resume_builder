from langchain.agents import create_agent
from langchain.tools import tool, ToolRuntime
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langchain_core.runnables import RunnableConfig

from resume_builder.constants import AvailableModel
from resume_builder.utils import get_ollama_model, StreamObj, MemoryProvider
from resume_builder.tools import (
    read_local_pdf_file,
    get_file_management_toolkit,
    get_proper_interrupt,
)
from resume_builder.system_prompts import PDF_TO_LATEX_PROMPT, LATX_TO_MATCH_JD
from resume_builder.stream.stream import stream


@tool(name_or_callable="get_user_input")
def get_user_input_tool(query: str = "") -> str:
    """
    This tool will help you to get input form user.
    You need to provide what you need from the user in query parameter
    Args:
        runtime (ToolRuntime): Optional

    Returns:
        str: User Input
    """
    return input(query)


@tool(name_or_callable="customize_latax_with_jd")
def personalize_latex_with_jd_tool(
    job_description: str, config: RunnableConfig, runtime: ToolRuntime
):
    """
    This agent tool with help you to tailor your latex resume to match the given job_description(jd)
    """
    model = get_ollama_model(AvailableModel.qwen_3_5_4_b)
    tools = get_file_management_toolkit()
    tools.append(get_user_input_tool)

    writer = runtime.stream_writer
    writer(f"Invoking personalized latex with jd tool")

    interrupt_on = get_proper_interrupt(tools=tools)

    hitl_middleware = HumanInTheLoopMiddleware(interrupt_on=interrupt_on)

    agent = create_agent(
        model=model,
        tools=tools,
        middleware=[hitl_middleware],
        checkpointer=MemoryProvider().checkpointer,
        system_prompt=LATX_TO_MATCH_JD,
    )

    stream_obj = StreamObj(agent=agent)
    stream(job_description, config=config, **stream_obj.model_dump())


@tool(name_or_callable="pdf_to_latex")
def pdf_to_latex_agent_tool(query: str, config: RunnableConfig, runtime: ToolRuntime):
    """
    This agent will help you to convert pdf to latex
    You should also provide query value
    """
    model = get_ollama_model(AvailableModel.qwen_3_5_4_b)
    tools = [read_local_pdf_file]

    writer = runtime.stream_writer
    writer(f"Invoking pdf_to_latex_agent")

    interrupt_on = get_proper_interrupt(tools=tools)
    hitl_middleware = HumanInTheLoopMiddleware(interrupt_on=interrupt_on)

    agent = create_agent(
        model=model,
        tools=tools,
        middleware=[hitl_middleware],
        checkpointer=MemoryProvider().checkpointer,
        system_prompt=PDF_TO_LATEX_PROMPT,
    )

    stream_obj = StreamObj(agent=agent, config=config)
    stream(query, **stream_obj.model_dump())
