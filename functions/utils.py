

import json

from .album_queries import (
    get_album_by_title,
    get_album_by_artists,
    get_album_by_year,
    get_album_by_genre,
    get_album_by_generated_query,
    
)
from .file_operations import read_csv_file

#get the function to call
def getFunctiontocall(functionname: str):
    function_map = {
        "get_album_by_title": get_album_by_title,
        "get_album_by_artists": get_album_by_artists,
        "get_album_by_genre": get_album_by_genre,
        "get_album_by_year": get_album_by_year,
        "get_album_by_generated_query": get_album_by_generated_query,
        "read_csv_file": read_csv_file
    }
    return (function_map[functionname])

#check if function exist
def isfunctionexist(functionname: str):
    available_functions = {
        "get_album_by_title",
        "get_album_by_artists",
        "get_album_by_genre",
        "get_album_by_year",
        "get_album_by_generated_query",
        "read_csv_file"
    }
    return (functionname in available_functions)
