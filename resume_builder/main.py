from resume_builder.agent import get_file_system_explorer_agent
from resume_builder.stream.stream import stream
from resume_builder.constants import StreamMode
import uuid
import asyncio

async def async_main() -> None:
    agent = get_file_system_explorer_agent()
    session_id = str(uuid.uuid4())
    config = {
        "configurable": {"thread_id": session_id}
    }  # It is requried for human in the loop conversation
    stream_modes = [mode.value for mode in StreamMode]
    version = "v2"
    print("start streaming")
    stream(
        agent=agent,
        stream_mode=stream_modes,
        version=version,
        config=config,
        show_tool_output=False
    )
    print()

def main():
    asyncio.run(async_main())


if __name__ == "__main__":
    asyncio.run(async_main())
