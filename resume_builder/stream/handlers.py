from langgraph.types import Command
from resume_builder.constants import DecisionType


def handle_messages(chunk):
    data, _metadata = chunk["data"]
    if data.content:
        print(data.content, end="", flush=True)


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
        return Command(resume={"decisions": [{"type": DecisionType.approve}]})

    return Command(
        resume={
            "decisions": [
                {
                    "type": DecisionType.reject,
                    "comment": (
                        "User denied access to this file. Do not try to read it again. "
                        "Provide a response based only on what you already know."
                    ),
                }
            ]
        }
    )


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
