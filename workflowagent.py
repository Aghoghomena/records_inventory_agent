from openai import OpenAI
from functions import create_tools, get_album_by_artists, get_album_by_title,isfunctionexist, getFunctiontocall, get_album_by_genre, get_album_by_year, get_album_by_generated_query,read_csv_file, write_csv_file
from functions.chat_ai import get_chat_response
from functions.state import conversation_history,add_system, add_user,append_tool_response,append_function_response, append_to_format
from langsmith import traceable
from config import client, model
import json


EXIT_KEYWORDS = ["goodbye", "bye", "exit", "quit", "done", "thank you", "thanks", "no more", "that's all"]
output = {"enquiry":str, "response":str}
email_output_csv =[]

#add  multi language
@traceable(name ="multi_turn_conversation")
def multi_turn_conversation():
    "Welcome to RetroGroove Records"
    # Initialize conversation with system prompt
    add_system(
            "You are VinylBot, a friendly and knowledgeable assistant warm and helpful working at RetroGroove Records"
            "Your role is to help customers with album availability, artist queries, and personalized record recommendations."
            "Once the user says nothing else or words like no, thank you, thats all or they need no more assistant you can end and say goodbye terminate all calls to Gemini"
            "The first thing to do is to call read a csv file and get the contents of the csv file to get the user's queries and questions"
            "Loop through each of the user's queries and questions and call the appropriate tool to get the albums and respond to the user"
            "You have access to multiple tools-> get_album_by_genre(for simple genre or subgenre queries), get_album_by_year(for simple year, date range or decade queries, for date only queries), "
            "get_album_by_generated_query(for multiple queries or filter like year and artist,e “rock albums from the early 70s ), get_album_by_artists(for artist-only queries), "
            "after getting the function response format it and present the output to the user in a human readable ordered list format as a conversation response"
        )
    #add user message to read csv file
    add_user("read the csv data to get the user's queries and questions call the read csv file tool")
# Call the chat to get the tool to read the csv
    response = get_chat_response()
    append_tool_response(response)
    #this is a single function call to read csv file
    print("\n=== Tool Call Response for read_csv_file ===")
    print(response.tool_calls)
    read_csv_tool = response.tool_calls[0]
    #going to skip checking if function exists for read csv file as its a single 
    function_to_call = getFunctiontocall(read_csv_tool.function.name)
    cust_enquirys = function_to_call(**json.loads(read_csv_tool.function.arguments))
    #add function response to conversation history
    append_function_response(read_csv_tool.id,read_csv_tool.function.name, cust_enquirys)
    #loop through each of the user's queries and questions and answer them
    for enquiry in cust_enquirys['rows']:
        # Call the chat to get the tool to answer the user's query
        print("\n=== New User Enquiry ===")
        print(enquiry)
        add_user(enquiry)
        print("\n=== Getting Chat Response for User Enquiry ===")
        response = get_chat_response()
        append_tool_response(response)
        # Check if there are tool calls in the response
        if response.tool_calls:
            for tool_call in response.tool_calls:
                # Check if the function exists
                if isfunctionexist(tool_call.function.name):
                    function_to_call = getFunctiontocall(tool_call.function.name)
                    functionargs =json.loads(tool_call.function.arguments)
                    function_response = function_to_call(**functionargs)
                    #add function response to conversation history
                    append_function_response(tool_call.id,tool_call.function.name, function_response)
                    get_chat_response_function = get_chat_response()
                    #format the function response for better presentation
                    append_to_format(function_response)
                    #get the chat after function response
                    get_chat_response_format_output = get_chat_response()
                    print(get_chat_response_format_output)
                    email_output_csv.append({
                        "enquiry": enquiry,
                        "response": get_chat_response_format_output.content
                    })
                    add_user(get_chat_response_format_output.content)
                    print("\n=== Final Response to each user call ===")
                else:
                    tool_response = f"Function {tool_call.function.name} does not exist."
                    append_function_response(tool_call.id,tool_call.function.name, tool_response)
            print("\n=== End New User Enquiry ===")
        else:
            print("No tool calls in the response.")
    add_user("I have no more questions, thank you.")
    get_chat_response()




 
response = multi_turn_conversation()
print("\n=== Conversation Ended ===")
#write the email output to a csv file
write_response = write_csv_file("resources/email_responses.csv", email_output_csv)