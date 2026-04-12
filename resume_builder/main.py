from resume_builder.agents.orchestrator import orchestrator_agent
from resume_builder.stream.stream import stream
from resume_builder.utils import StreamObj, get_user_input
import asyncio


async def async_main() -> None:
    agent = orchestrator_agent()
    stream_obj = StreamObj(agent=agent)
    user_input = get_user_input()
    print("start streaming")
    stream(user_input, **stream_obj.model_dump())
    print()


def main():
    asyncio.run(async_main())


if __name__ == "__main__":
    asyncio.run(async_main())
