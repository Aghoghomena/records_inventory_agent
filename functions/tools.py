# define the tools
from typing import List, Dict, Any, Optional


def create_tools() -> List[Dict[str, Any]]:
    
    db_tools =[
        {
            "type": "function",
            "function": {
                "name": "get_album_by_title",
                "description": "When a string that contains an album title is passed, search the database in local using function get_album_by_title and return the details of the row with the string as an album. Search the database for albums by title. Returns details of all matching albums including year, artist, genre, subgenre, and price.",
                "parameters": {
                    "type": "object",
                    "properties":{
                        "title": {
                            "type" : "string",
                            "description": "the name or title of an album e.g London Calling"
                        }
                    },
                    "required": ["title"],
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_album_by_artists",
                "description": "When a user asks about one or more artists album e.g (Do you have any Bowie or Beyonce, Any Prince Album)"
                "call this tool extract the names and store in an array with artists names used to search the local database",
                "parameters": {
                    "type": "object",
                    "properties":{
                        "artists": {
                            "type" : "array",
                            "items": {"type": "string"},
                            "description": "The list of artist names to search for (e.g ['Beyonce', 'Taylor Swift'])"
                        },
                    },
                    "required": ["artists"],
                }
            }
        },
         {
            "type": "function",
            "function": {
                "name": "get_album_by_year",
                "description": "When a user mentions or asks for a specific year (for example: 'give me albums from 1982'), or time range such as the 90's or early 70s or late 90s"
                "This should be called when the year or date range the range_end and range_start or year is mentioned in the user query"
                "call this function to search the local database for albums released in that year."
                "if a specific year is given return albums released in that year"
                "if a time range then convert it into a range and return all albums within that range",
                "parameters": {
                    "type": "object",
                    "properties":{
                        "year": {
                            "type" : "integer",
                            "description": "The specific year passed to search for such as 1967 "
                        },
                        "range_start": {
                            "type" : "integer",
                            "description": "The start of time range e.g late 90s is 1997"
                        },
                        "range_end": {
                            "type" : "integer",
                            "description": "The end of time range e.g late 90s is 1999"
                        },
                    },
                    "required": [],
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_album_by_genre",
                "description": "When a user asks exclusively about a genre or subgenre, extract the genre and search the database using the genre or subgenre for all albums in those categories. Returns a list of all albums by that artist including title, year, genre, subgenre, and price. if its an empty list return a conversation response as a customer support"
                "This should be called when a single query genre or subgenre is asked"
                "if it has albums return the list of albums in an unordered list and continue the conversation",
                "parameters": {
                    "type": "object",
                    "properties":{
                        "genre": {
                            "type" : "string",
                            "description": "The genre or subgenre of the album (e.g., 'Rock', Soft Rock)"
                        },
                    },
                    "required": ["genre"],
                }
            }
        },
         {
            "type": "function",
            "function": {
                "name": "get_album_by_generated_query",
                "description": "When a user asks questions and no tool fits or applies or when there is multiple queries such as the year and artist, this should be called as last resort"
                "Use this to convert users query to an SQLite query that selects all from music class and where matches the condition based on user input"
                "It returns the query as a string which is passed to get_album_by_generated_query"
                "An example give me Beyonce Album in 1990 then select * from music where artist='Beyonce' and year = 1990",
                "parameters": {
                    "type": "object",
                    "properties":{
                        "generated_query": {
                            "type" : "string",
                            "description": "The SQLite query generated from users input to get a list of Albums"
                        },
                    },
                    "required": ["generated_query"],
                }
            }
        },
          {
            "type": "function",
            "function": {
                "name": "read_csv_file",
                "description": f"This takes in the csv in path resources/emails.csv and reads the csv file."
                "The file contains customer email queries and responses. We will get all the emails sent in which will be our conversation",
                "parameters": {
                    "type": "object",
                    "properties":{
                        "file_path": {
                            "type" : "string",
                            "description": "The path to the csv to read"
                        },
                    },
                    "required": ["file_path"],
                }
            }
        },

        {
            "type": "function",
            "function": {
                "name": "format_album_list_response",
                "description": f"This takes in a list of albums and formats to a human readable answer. This uses AI to format the output. this uses no other function except AI to format the output."
                "Given [{{'album': 'Album1', 'artist': 'Artist1', 'year': 2000}, {{'album': 'Album2', 'artist': 'Artist2', 'year': 2001}}], return a formatted string like we have what you are looking for '* Hunky Dory (1971)'."
                "Format this album list into clean bullet points. the AI should do the formatting",
                "parameters": {
                    "type": "object",
                    "properties":{
                        "albums": {
                            "type" : "array",
                            "description": "The list of album dictionaries returned from album query functions",
                        },
                    },
                    "required": ["albums"],
                }
            }
        }

    ]
    return db_tools





