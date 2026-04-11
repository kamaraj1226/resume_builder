from resume_builder.agent import get_general_agent


def main():
    agent = get_general_agent()
    user_input = (
        "can you use read_local_file tool and read /mnt/d/resume_building/Dockerfile in the current directory"
    )
    agent_input = {"messages": [{"role": "user", "content": user_input}]}
    stream_mode = ["updates", "custom", "messages"]
    version = "v2"
    stream_chunks = agent.stream(agent_input, stream_mode=stream_mode, version=version)
    print("start streaming")
    for chunk in stream_chunks:
        # print(f"stream_mode: {chunk['type']}", flush=True)
        # print(f"content: {chunk['data']}", flush=True)

        if chunk['type'] == 'custom':
            print(f"Custom chunk data: {chunk['data']}")

        if chunk["type"] == "messages":
            data, _metadata = chunk["data"]
            if data.content:
                print(data.content, end="", flush=True)
    print()


if __name__ == "__main__":
    main()
