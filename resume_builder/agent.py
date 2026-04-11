from langchain.agents import create_agent
from resume_builder.tools import read_local_file
from resume_builder.utils import get_ollama_model

def get_general_agent():
    model = get_ollama_model()

    agent = create_agent(
        model = model,
        tools = [read_local_file],
        
    )

    return agent