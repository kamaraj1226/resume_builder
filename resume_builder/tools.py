from langchain.tools import tool, ToolRuntime
from resume_builder.mcp_client.duckduckgo_mcp_client import get_dkdkg_client_tools
from pathlib import Path

# Read local file
@tool(name_or_callable='read_local_pdf_file')
def read_local_pdf_file(file_path: str, runtime: ToolRuntime) -> str:
    """
    Read local pdf file. This tool have the ability to read local pdf file
    It won't extract or understands image.

    Args:
        file_path (str): local pdf filepath

    Raises:
        Exception: If file is not found it will raise File not found exception

    Returns:
        str: Return file content if exists
    """
    import fitz
    path = Path(file_path)
    writer = runtime.stream_writer
    writer(f"Reading pdf file ==================: {path.name}")

    if not path.is_file():
        raise Exception(f"File not found: {file_path}")
    
    with fitz.open(path) as doc:
        return ''.join([page.get_text() for page in doc])
    
    return ''

# Read local file
@tool(name_or_callable="read_local_file")
def read_local_file(file_path: str, runtime: ToolRuntime) -> str:
    """
    Tool have the ability to read the local file

    Args:
        file_path (str): file path it should be of type python str

    Raises:
        Exception: If file is not found it will raise File not found exception

    Returns:
        str: Return file content if exists
    """
    path = Path(file_path)
    writer = runtime.stream_writer
    writer(f"Reading ==================: {path.name}")

    if not path.is_file():
        raise Exception(f"File not found: {file_path}")
    
    content = path.read_text(encoding='utf-8')
    return content
    
def get_current_working_dir() -> str:
    current_working_dir  = str(Path.cwd().resolve(strict=True))
    return current_working_dir

async def dkdkg_web_search_tools():
    return await get_dkdkg_client_tools()