from openai import OpenAI, pydantic_function_tool
from functions import create_tools, get_album_by_artists, get_album_by_title,isfunctionexist, getFunctiontocall, get_album_by_genre, get_album_by_year, get_album_by_generated_query,read_csv_file, write_csv_file, write_text_to_csv
from functions.chat_ai import get_chat_response
from functions.state import conversation_history,add_system, add_user,append_tool_response,append_function_response, append_to_format, add_assistant, append_single_tool_response
from langsmith import traceable
from config import client, model
import json
from pydantic import BaseModel, Field
import csv



@traceable(name="react Workflow")
def execute_function(tool_call):
    if isfunctionexist(tool_call.function.name):
        function_name = getFunctiontocall(tool_call.function.name)
        args = json.loads(tool_call.function.arguments)
        function_output = function_name(**args)
        return function_output
    else:
        return {"error": f"Function {tool_call.function.name} does not exist."}

@traceable(name ="read_csv_file_tool")
def process_csv_file(conversation_history):
    while True:
        response = client.chat.completions.create(
            model=model,
            messages=conversation_history,
            tools=create_tools()
        )
        ## get the tool calls from the response
        output = response.choices[0].message
        print("\n=== Tool Calls to Process ===")
        print(output)
        if not output.tool_calls:
            add_assistant(response.choices[0].message.content)
            break

        # execute each tool call and append the result to the messages
        for tool_call in output.tool_calls:
            print("\n=== Executing Tool Call ===")
            print(tool_call)
            tool_response = execute_function(tool_call)
            print(f"\n🔧 Function: {tool_call.function.name} Response: {tool_response}")
            append_single_tool_response(tool_call)
            conversation_history.append({
                "role": "function",
                "name": tool_call.function.name,
                "content": json.dumps(tool_response)
            })
    return response


add_system("You are a helpful assistant that reads customers queries and processes."
           "You have access to multiple tools-> get_album_by_genre(for simple genre or subgenre queries), get_album_by_year(for simple year, date range or decade queries, for date only queries), "
          "get_album_by_generated_query(for multiple queries or filter like year and artist,e “rock albums from the early 70s ), get_album_by_artists(for artist-only queries), "
         "after getting the function response format it and present the output to the user in a human readable ordered list format as a conversation response"
         "You handle the routing of each of the user's queries and questions to the appropriate tool and function and tool calls "
    )
add_user("read the csv file resources/emails.csv to get the user's queries, it gives a Python dictionary with a key named rows, process the dictionary and get a Python-style list of enquiries. "
        "loop through the Python-style list of enquiries and process them one by one calling the appropriate tools. "
        "Return a list of albums for each enquiry using the appropriate tool and function and return the response in a human readable ordered list format as a conversation response"
        "for each enquiry"
        "1. call the appropriate tool to get the albums"
        "2. call the functtion to get the albums"
        "3. format the function response for better presentation and use as the response to the user"
        '4. return the query and response to the user as part of the conversation'
        "5. after processing all the enquiries write the list of enquiries and responses return as output"
     )

load =process_csv_file(conversation_history)
print("\n=== Final Conversation Output ===")
print(load.choices[0].message.content)
write_text_to_csv("resources/email_responses_2.csv", load.choices[0].message.content)
 