# functions/state.py
from typing import List, Dict, Any
import json

# Global, module-level singleton
conversation_history: List[Dict[str, Any]] = []

def reset_history():
    conversation_history.clear()

def add_user(content: str):
    conversation_history.append({"role": "user", "content": content})

def add_system(content: str):
    conversation_history.append({"role": "system", "content": content})

def add_assistant(content: str, tool_calls: List[Dict[str, Any]] | None = None):
    conversation_history.append({"role": "assistant", "content": content})

def append_tool_response(response):
    print(response.tool_calls)
    conversation_history.append({
        "role": "assistant",
        "content": response.content,
        "tool_calls": [
                        {
                            "id": tool_call.id,
                            "type": tool_call.type,
                            "function": {
                                "name": tool_call.function.name,
                                "arguments": tool_call.function.arguments
                            }
                        }
                         for tool_call in response.tool_calls
                    ]
    })

def append_function_response(tool_call_id: str, functionname: str, function_result):
    conversation_history.append({
        "role": "function",
        "tool_call_id": tool_call_id,
        "name": functionname,
        "content": json.dumps(function_result)
    })

    print("\n=== End Appending Function Response to Conversation History End ===")

def append_to_formatt(response):
     #append if function is not read_csv to format the output
    conversation_history.append({
    "role": "assistant",
    "content": "",
    "tool_calls": [
        {
            "id": "format_album_list_response",
            "type": "function",
            "function": {
                "name": "format_album_list_response",
                "arguments": json.dumps({"albums": response})
            }
        }
    ]
})
    
def append_to_format(response):
    """
    Ask the model to format the latest tool output.
    """
    conversation_history.append({
        "role": "user",
        "content": (
            "Please take the tool result from and turn the album list into a friendly, "
            "human-readable answer. If the data is empty, let the customer know we "
            "didn't find anything yet and invite follow-up questions.\n\n"
            "Tool result:\n"
            f"{json.dumps(response, indent=2, ensure_ascii=False)}"
        )
    })


def append_single_tool_response(tool_call):
    print(tool_call)
    conversation_history.append({
        "role": "assistant",
        "content": None,
        "tool_calls": [
                        {
                            "id": tool_call.id,
                            "function": {
                                "name": tool_call.function.name,
                                "arguments": tool_call.function.arguments
                            }
                        }
                    ]
    })
