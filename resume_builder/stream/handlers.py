from langgraph.types import Command
from resume_builder.constants import DecisionType


def handle_messages(chunk):
    data, _metadata = chunk["data"]
    if data.content:
        print(data.content, end="", flush=True)


def handle_updates(chunk):
    if "__interrupt__" not in chunk["data"]:
        return None

    interrupt_item = chunk["data"]["__interrupt__"][0]
    details = interrupt_item.value
    action_requests = details.get("action_requests", [])

    if not action_requests:
        return None

    decisions = []

    print(f"\n[PAUSED - {len(action_requests)} Actions Pending]")

    for request in action_requests:
        action = request.get("name")
        args = request.get("args")
        tool_id = request.get("id")

        print(f"\nTool: {action} | Args: {args}")
        choice = input("Approve (y), Reject (n), or Edit (e)? ").strip().lower()

        if choice == "y":
            decisions.append({"type": "approve", "id": tool_id})

        elif choice == "e":
            new_args = {}
            for key, val in args.items():
                u_input = input(f"  {key} [{val}]: ").strip()
                new_args[key] = u_input if u_input != "" else val

            # Match the schema the middleware expects
            edited_action = request.copy()
            edited_action["args"] = new_args
            decisions.append(
                {"type": "edit", "id": tool_id, "edited_action": edited_action}
            )

        else:
            reason = input("Explain why: ")
            decisions.append(
                {"type": "reject", "id": tool_id, "comment": reason or "User rejected."}
            )

    # Return ALL decisions at once
    return Command(resume={"decisions": decisions})


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
