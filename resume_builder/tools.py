from langchain.tools import tool, ToolRuntime
from pathlib import Path

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
    
