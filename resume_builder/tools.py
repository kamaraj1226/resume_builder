from langchain.tools import tool, ToolRuntime
from resume_builder.mcp_client.duckduckgo_mcp_client import get_dkdkg_client_tools
from pathlib import Path


# Read local file
@tool(name_or_callable="read_pdf_file")
def read_pdf_file(file_path: str, runtime: ToolRuntime) -> str:
    """
    Read local pdf file. This tool have the ability to read local pdf file
    It won't extract or understands image.

    Args:
        file_path (str): local pdf filepath
    Returns:
        str: Return file content if exists
    """
    import fitz

    path = Path(file_path).expanduser().resolve()
    writer = runtime.stream_writer
    writer(f"Reading pdf file ==================: {path.name}")

    if not path.is_file():
        return (
            f"File not found: {file_path}. Please check the provided path."
            "You may need to include './' at the begining if you are using relative path"
            f"path is resolved to {path}"
        )

    with fitz.open(path) as doc:
        return "".join([page.get_text() for page in doc])

    return ""


# Read local file
@tool(name_or_callable="read_simple_file")
def read_simple_file(file_path: str, runtime: ToolRuntime) -> str:
    """
    Tool have the ability to read simple local file
    Can't able to read complex files like pdf, word or other types of file.

    Args:
        file_path (str): file path it should be of type python str

    Returns:
        str: Return file content if exists or error message
    """
    path = Path(file_path)
    writer = runtime.stream_writer
    writer(f"Reading ==================: {path.name}")

    if not path.is_file():
        # Handling this in safe mode
        return (
            f"File not found: {file_path}. Please check the provided path."
            "You may need to include './' at the begining if you are using relative path"
        )

    content = path.read_text(encoding="utf-8")
    return content


def get_current_working_dir() -> str:
    current_working_dir = str(Path.cwd().resolve(strict=True))
    return current_working_dir


import os
from langchain_community.agent_toolkits import FileManagementToolkit
from resume_builder.constants import TRUSTED_TOOLS


def get_file_management_toolkit():
    working_dir = get_current_working_dir()
    working_dir = "/mnt/d/resume_building/resume_builder/files"  # Temporarly overriding to custom directory
    os.makedirs(working_dir, exist_ok=True)
    toolkit = FileManagementToolkit(root_dir=working_dir)
    tools = toolkit.get_tools()
    return tools


from typing import List, Dict


def get_proper_interrupt(tools: List) -> Dict[str, bool]:
    interrupt_on = {_tool.name: _tool.name not in TRUSTED_TOOLS for _tool in tools}
    return interrupt_on


async def dkdkg_web_search_tools():
    return await get_dkdkg_client_tools()
