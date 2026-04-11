from resume_builder.utils import get_user_input
from resume_builder.constants import StreamMode
from resume_builder.stream.handlers import handle_messages, handle_updates

def stream(agent, stream_mode, version, config, show_tool_output=True):
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
            chunk_type = chunk['type']
            if chunk_type == StreamMode.messages.value:
                role_state[0] = handle_messages(
                    chunk, show_tool_output, last_role_container=role_state
                )

            elif chunk_type == StreamMode.updates.value:
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