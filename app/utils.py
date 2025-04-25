# app/utils.py

def parse_agent_response(response):
    """
    Extracts the relevant text and tool call info from the agent's response.
    """
    messages = response.get("messages", [])
    print("DEBUG: messages =", messages)
    ai_message = next((m for m in messages if m.__class__.__name__ == "AIMessage"), None)
    if not ai_message:
        return "No AI response found."

    # Extract main text
    text = getattr(ai_message, "content", "")

    # Extract tool call info if present
    tool_info = ""
    # Tool call info may be in additional_kwargs or response_metadata
    if hasattr(ai_message, "additional_kwargs") and ai_message.additional_kwargs:
        tool_info = str(ai_message.additional_kwargs)
    elif hasattr(ai_message, "response_metadata") and ai_message.response_metadata:
        tool_info = str(ai_message.response_metadata)

    # Format output
    if tool_info:
        return f"{text}\n\n[Tool Info: {tool_info}]"
    else:
        return text