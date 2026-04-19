from pathlib import Path
from langchain_community.agent_toolkits import FileManagementToolkit
from resume_builder.constants import TRUSTED_TOOLS
from typing import Dict, List
from langchain.tools import ToolRuntime, tool
from resume_builder.mcp_client.duckduckgo_mcp_client import get_dkdkg_client_tools


@tool
def read_pdf_file(file_path: str, runtime: ToolRuntime = None) -> str:
    """
    Read local PDF files.
    Args:
        file_path (str): The local pdf filepath starting with / (e.g., '/document.pdf')
        runtime (ToolRuntime): Injected automatically by the agent.
    """
    import fitz  # PyMuPDF

    # Use stream_writer if available for logging, else fallback to print
    writer = getattr(runtime, "stream_writer", print)
    writer(f"Attempting to open PDF: {file_path}")

    try:
        # Deep Agents injects the backend into the runtime context
        backend = None
        if runtime:
            # Try standard DeepAgents service lookup
            if hasattr(runtime, "get_service"):
                backend = runtime.get_service("backend")
            # Try direct attribute access
            elif hasattr(runtime, "backend"):
                backend = runtime.backend
            # Try nested services object
            elif hasattr(runtime, "services"):
                backend = getattr(runtime.services, "backend", None)

        if backend:
            # backend.read_file handles the virtual root (/) mapping
            file_bytes = backend.read_file(file_path)
            if isinstance(file_bytes, str):
                file_bytes = file_bytes.encode("utf-8", errors="ignore")
        else:
            # Manual fallback: Look in the physical ./files folder
            actual_path = Path("./files") / file_path.lstrip("/")
            with open(actual_path, "rb") as f:
                file_bytes = f.read()

        # Extract text using PyMuPDF
        with fitz.open(stream=file_bytes, filetype="pdf") as doc:
            text = "".join([page.get_text() for page in doc])

        return text if text.strip() else "The PDF is empty or only contains images."

    except FileNotFoundError:
        return f"Error: File '{file_path}' not found in the workspace."
    except Exception as e:
        return f"Error reading PDF: {str(e)}"


def get_current_working_dir() -> str:
    current_working_dir = str(Path.cwd().resolve(strict=True))
    return current_working_dir


def get_proper_interrupt(tools: List) -> Dict[str, bool]:
    interrupt_on = {_tool.name: _tool.name not in TRUSTED_TOOLS for _tool in tools}
    return interrupt_on


async def dkdkg_web_search_tools():
    return await get_dkdkg_client_tools()
