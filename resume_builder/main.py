from resume_builder.agent import get_general_agent, get_file_system_explorer_agent


def sample_code():
    agent = get_general_agent()
    user_input = "can you use read_local_file tool and read /mnt/d/resume_building/Dockerfile in the current directory"
    agent_input = {"messages": [{"role": "user", "content": user_input}]}
    stream_mode = ["updates", "custom", "messages"]
    version = "v2"
    stream_chunks = agent.stream(agent_input, stream_mode=stream_mode, version=version)
    print("start streaming")
    for chunk in stream_chunks:
        # print(f"stream_mode: {chunk['type']}", flush=True)
        # print(f"content: {chunk['data']}", flush=True)

        if chunk["type"] == "custom":
            print(f"Custom chunk data: {chunk['data']}")

        if chunk["type"] == "messages":
            data, _metadata = chunk["data"]
            if data.content:
                print(data.content, end="", flush=True)
    print()


import uuid


def get_user_input():
    user_input = "can you use read_file tool and read /mnt/d/resume_building/Dockerfile in the current directory"
    return user_input


def handle_messages(chunk):
    data, _metadata = chunk["data"]
    if data.content:
        print(data.content, end="", flush=True)


from langgraph.types import Command


def handle_updates(chunk):
    if "__interrupt__" not in chunk["data"]:
        return None

    # 1. Unpack the first Interrupt object from the tuple
    # chunk['data']['__interrupt__'] is (Interrupt(value=...),)
    interrupt_item = chunk["data"]["__interrupt__"][0]

    # 2. Access the value (the dictionary we saw in your debug)
    details = interrupt_item.value

    # 3. Extract the first action request for display
    action_requests = details.get("action_requests", [])
    if action_requests:
        first_request = action_requests[0]
        action = first_request.get("name", "Unknown")
        args = first_request.get("args", {})
    else:
        return None

    print(f"\n[PAUSED - Approval Required]")
    print(f"Tool: {action} | Arguments: {args}")

    choice = input("Approve? (y/n): ").strip().lower()

    # 4. Return the structured dictionary required by the middleware
    if choice == "y":
        return Command(resume={"decisions": [{"type": "approve"}]})

    return Command(
        resume={
            "decisions": [
                {
                    "type": "reject",
                    "comment": "User denied access to this file. Do not try to read it again. Provide a response based only on what you already know.",
                }
            ]
        }
    )


from langgraph.types import Command


def handle_messages(chunk, show_tool_output=True, last_role_container=None):
    data, metadata = chunk["data"]

    # 1. Identify the role using the most reliable metadata fields
    # LangGraph v2 metadata usually contains 'langgraph_node'
    node_name = metadata.get("langgraph_node", "")

    # In most agents, tool results come from a node named 'tools'
    is_tool_chunk = node_name == "tools" or getattr(data, "role", "") == "tool"

    if is_tool_chunk:
        if show_tool_output and data.content:
            print(data.content, end="", flush=True)
        return "tool"

    # If it's not a tool and has content, it's the AI speaking
    if data.content:
        # Check if we need to force a newline because the last chunk was a tool
        if last_role_container and last_role_container[0] == "tool":
            print("\n", flush=True)
            last_role_container[0] = "ai"  # Reset so we don't spam newlines

        print(data.content, end="", flush=True)
        return "ai"

    return last_role_container[0] if last_role_container else None


def stream(agent, stream_mode, version, config, show_tool_output=False):
    user_input = get_user_input()
    agent_input = {"messages": [{"role": "user", "content": user_input}]}

    # Use a list to pass role by reference so handle_messages can update it
    role_state = [None]

    while True:
        next_command = None
        stream_chunks = agent.stream(
            agent_input, stream_mode=stream_mode, version=version, config=config
        )

        for chunk in stream_chunks:
            if chunk["type"] == "messages":
                role_state[0] = handle_messages(
                    chunk, show_tool_output, last_role_container=role_state
                )

            elif chunk["type"] == "updates":
                next_command = handle_updates(chunk=chunk)
                if next_command:
                    print("\n", flush=True)
                    role_state[0] = "interrupt"  # Mark state
                    break

        if next_command:
            agent_input = next_command
        else:
            print()
            break


def main():
    agent = get_file_system_explorer_agent()
    session_id = str(uuid.uuid4())
    config = {
        "configurable": {"thread_id": session_id}
    }  # It is requried for human in the loop conversation
    stream_mode = ["updates", "custom", "messages"]
    version = "v2"
    print("start streaming")
    stream(agent=agent, stream_mode=stream_mode, version=version, config=config)
    print()


if __name__ == "__main__":
    main()
