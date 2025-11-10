from openai import OpenAI
from config import client, model
from .tools import create_tools
from .state import conversation_history




def get_chat_response():

    response = client.chat.completions.create(
        model=model,
        messages=conversation_history,
        tools=create_tools()
    )

    # Extract the assistant's message safely
    message = response.choices[0].message
    print("\n=== AI Response from call ===")
    print(message)
    print("=== End of AI Response ===\n")
    return message

