from langchain.agents import create_agent
from resume_builder.tools import read_local_file
from resume_builder.utils import get_ollama_model
from langchain_community.agent_toolkits import FileManagementToolkit
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langgraph.checkpoint.memory import InMemorySaver
from resume_builder.tools import get_current_working_dir
import os

def get_general_agent():
    model = get_ollama_model()

    agent = create_agent(
        model = model,
        tools = [read_local_file],
        
    )
    return agent

def get_file_system_explorer_agent():
    model = get_ollama_model()
    working_dir = get_current_working_dir()
    os.makedirs(working_dir, exist_ok=True)
    toolkit = FileManagementToolkit(root_dir=working_dir)
    tools = toolkit.get_tools()

    # human in the loop middleware
    interrupt_on = {tool.name : True for tool in tools}
    interrupt_on['list_directory'] = False # No interrupts to list the directory
    interrupt_on['read_file'] = False # No problem in reading file except bloating context memory

    hitl_middleware = HumanInTheLoopMiddleware(
        interrupt_on=interrupt_on
    )

    agent = create_agent(
        model=model,
        tools = tools,
        middleware=[hitl_middleware],
        checkpointer=InMemorySaver()
    )
    return agent
