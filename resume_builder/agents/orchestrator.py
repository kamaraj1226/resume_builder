from pathlib import Path
from deepagents import create_deep_agent
from deepagents.backends import FilesystemBackend
from langchain.agents.middleware import HumanInTheLoopMiddleware

from resume_builder.utils import get_ollama_model, MemoryProvider
from resume_builder.agents.agent_as_tools import read_pdf_file
from resume_builder.tools import get_proper_interrupt
from resume_builder.system_prompts import ORCHESTRATOR


def orchestrator_agent():
    model = get_ollama_model()

    root_file_dir = Path("./files").resolve()
    root_file_dir.mkdir(parents=True, exist_ok=True)
    print(f"✅ Backend pointing to: {root_file_dir}")

    # Setup the Backend
    # 'virtual_mode=True' makes './files/test.txt' appear as '/test.txt' to the agent
    file_system_backend = FilesystemBackend(
        root_dir=str(root_file_dir), virtual_mode=True
    )

    # Setup Tools
    # We ONLY add custom tools. 'ls', 'read_file', 'write_file' are
    # automatically added by create_deep_agent because we provide a backend.
    custom_tools = [read_pdf_file]

    # Create the Agent
    # IMPORTANT: Do NOT manually add FilesystemMiddleware to the list.
    # create_deep_agent detects the 'backend' argument and adds it for you.
    agent = create_deep_agent(
        model=model,
        tools=custom_tools,
        backend=file_system_backend,  # This triggers the auto-tool generation
        middleware=[
            HumanInTheLoopMiddleware(
                interrupt_on=get_proper_interrupt(tools=custom_tools)
            )
        ],
        checkpointer=MemoryProvider().checkpointer,
        system_prompt=ORCHESTRATOR,
    )

    return agent
