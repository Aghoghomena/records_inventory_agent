from .connect_db import conn
from typing import List, Dict, Any, Optional



#get abulm by title
def get_album_by_title(title: str):
    #call the db to search 
    query = conn.cursor()

    try:
        query.execute("SELECT * FROM music WHERE album = ? COLLATE ", (title))
        rows = query.fetchall()
        # Convert tuples to dictionaries for better JSON serialization
        columns = ['number','year', 'album', 'artist', 'genre', 'subgenre', 'subgenre', 'price']
        return [dict(zip(columns, row)) for row in rows]
    except Exception as e:
        print(f"Error querying database: {e}")
        return []
    finally:
        query.close()

#get album by artists
def get_album_by_artists(artists):
    #call the db to search 
    if not artists:
         return []
    
    print("search by artists")
    query = conn.cursor()
    try:

        #process the artist
        like_condition_params = []
        like_conditions = []
        for artist in artists:
            artist_trimmed = artist.strip()
            if artist_trimmed:  # Only add if not empty after trimming
                like_conditions.append("artist LIKE ? COLLATE NOCASE")
                like_condition_params.append(f"%{artist_trimmed}%")

        if not like_conditions:
            return []
        
        where_clause = " OR ".join(like_conditions)
        queryvalue = f"SELECT * FROM music WHERE {where_clause}"

        print(f"Executing query: {queryvalue}")
        print(f"With parameters: {like_condition_params}")

        query.execute(queryvalue, like_condition_params)
        rows = query.fetchall()
        columns = ['number','year', 'album', 'artist', 'genre', 'subgenre', 'subgenre', 'price']
        return [dict(zip(columns, row)) for row in rows]
    except Exception as e:
            print(f"Error querying database: {e}")
            return []
    finally:
            query.close()


#get album by year or date
def get_album_by_year(year: int = None, range_start: int = None, range_end: int = None):
    #call the db to search 
    print("call album by year")
    query = conn.cursor()
    queryvalue = ""
    rows = []

    try:
        if year:
            queryvalue = "SELECT * FROM music WHERE year = year"
            print(queryvalue, ( year,))
            query.execute(queryvalue, ( year,))
            rows = query.fetchall()
        elif range_start and range_end:
             queryvalue = "SELECT * FROM music WHERE year Between ? AND ? "
             print(queryvalue, ( range_start, range_end))
             query.execute(queryvalue, ( range_start, range_end,))
             rows = query.fetchall()
        else:
             rows =[]
             
        columns = ['number','year', 'album', 'artist', 'genre', 'subgenre', 'subgenre', 'price']
        return [dict(zip(columns, row)) for row in rows]
    except Exception as e:
            print(f"Error querying database: {e}")
            return []
    finally:
            query.close()


#get album by genre
def get_album_by_genre(genre: str):
    #call the db to search 
    print("search by genre or subgenre")
    query = conn.cursor()
    try:
        queryvalue = "SELECT * FROM music WHERE genre LIKE '%' || TRIM(?) || '%' COLLATE NOCASE OR subgenre LIKE '%' || TRIM(?) || '%' COLLATE NOCASE"
        print(queryvalue, ( genre,))
        query.execute(queryvalue, ( genre, genre))
        rows = query.fetchall()
        columns = ['number','year', 'album', 'artist', 'genre', 'subgenre', 'subgenre', 'price']
        return [dict(zip(columns, row)) for row in rows]
    except Exception as e:
            print(f"Error querying database: {e}")
            return []
    finally:
            query.close()


#get album by gemini generate query
def get_album_by_generated_query(generated_query: str):
    #call the db to search 
    print("search gemini generated query")
    query = conn.cursor()
    try:

        print(generated_query)
        query.execute(generated_query)
        rows = query.fetchall()
        columns = ['number','year', 'album', 'artist', 'genre', 'subgenre', 'subgenre', 'price']
        return [dict(zip(columns, row)) for row in rows]
    except Exception as e:
            print(f"Error querying database: {e}")
            return []
    finally:
            query.close()
