from datetime import datetime

def login_user(conn, username, password):
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT passwordhash FROM users WHERE username = %s", (username,)
        )
        result = cursor.fetchone()
        if result and result[0] == password:
            last_access_date = datetime.now()
            cursor.execute(
                "UPDATE users SET last_access_date = %s WHERE username = %s",
                (last_access_date, username)
            )
            conn.commit()
            print(f"Login successful! Last access time updated to {last_access_date}")
        else:
            print("Invalid username or password.")
    except psycopg2.Error as e:
        print(f"An error occurred: {e}")
        conn.rollback()
    
# TODO: Auto increment ID
# create_user(connection, args.username, args.password, args.email, args.first_name, args.last_name)
def create_user(conn, username, password, email, first_name, last_name):
    cursor = conn.cursor()
    try:
        last_access_date = datetime.now()
        creation_date = datetime.now()
        print("inserting")
        cursor.execute(
            "INSERT INTO Users (user_id, last_access_date, creation_date, username, passwordhash, email, first_name, lastname) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (100000, last_access_date, creation_date, username, password, email, first_name, last_name)
        )
        conn.commit()
        print(f"Successfully created user {username}")
    except psycopg2.Error as e:
        print(f"An error occurred: {e}")
        conn.rollback()

def create_collection(conn, user_id, collection_name):
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO Collection (Collection_ID, name) VALUES (%s, %s)",
            (user_id, collection_name)
        )
        conn.commit()
        print(f"Collection '{collection_name}' created successfully.")
    except psycopg2.Error as e:
        print(f"An error occurred: {e}")
        conn.rollback()

'''
- Users will be to see the list of all their collections by name in ascending order. The list must show the following information per collection:
    - Collection’s name
    - # of movies in the collection
    - Total length of movies (hours:minutes) in the collection
'''
def list_collections(conn, user_id):
    cursor = conn.cursor()
    try:
        cursor.execute("""
            select c.name, count(m) as movie_count, sum(m.length) as total_length
            from collection c
            join holds h on c.collection_id = h.collection_id
            join movie m on m.movie_id=h.movie_id
            join users u on u.user_id=c.user_id
            where u.user_id=%s
            group by c.name
            """, [user_id])
        collections = cursor.fetchall()
        for collection_name, movie_count, total_length in collections:
            print(f"Collection: {collection_name}, Movies: {movie_count}, Total Length: {str(total_length)}")
    except psycopg2.Error as e:
        print(f"Error listing collections: {e}") 


'''
input 1: name, release date, cast members, studio, or genre
input 2: input string from above ^

input 3: sort by movie name, studio, genre, and released year (ascending and descending)

The resulting list of movies must show the movie’s name, the cast members, the
director, the length and the ratings (MPAA and user). The list must be sorted alpha-
betically (ascending) by movie’s name and release date

'''
def search_movies(conn, search_field, search_query, sort_field, sort_order):
    cursor = conn.cursor()

    # Mapping user input to database columns and tables for the search
    search_columns = {
        "name": "m.title",
        "release_date": "m.release_date",  # This column isn't defined in your structure, assuming it exists
        "cast_members": "c.first_name || ' ' || c.last_name",
        "studio": "s.studio_name",
        "genre": "g.genre_name"
    }

    # Mapping for sorting
    sort_columns = {
        "movie_name": "m.title",
        "studio": "s.studio_name",
        "genre": "g.genre_name",
        "released_year": "m.release_date"  # Assuming this column exists
    }

    # Validate inputs
    if search_field not in search_columns:
        raise ValueError(f"Invalid search field. Must be one of: {', '.join(search_columns.keys())}")
    
    if sort_field not in sort_columns:
        raise ValueError(f"Invalid sort field. Must be one of: {', '.join(sort_columns.keys())}")

    # Sorting order
    sort_order_sql = "ASC" if sort_order == "ascending" else "DESC"

    # Building the WHERE clause
    where_clause = f"{search_columns[search_field]} LIKE %s"

    # Construct the full SQL query
    sql_query = f"""
        SELECT m.title, STRING_AGG(c.first_name || ' ' || c.last_name, ', ') AS cast, 
               d.first_name || ' ' || d.last_name AS director, m.length, m.MPA_RATING,
               COALESCE(AVG(r.star_rating), 'Not Rated') AS user_rating
        FROM Movie m
        LEFT JOIN Acted_On ao ON m.Movie_ID = ao.Movie_id
        LEFT JOIN Contributors c ON ao.Contributor_id = c.contributor_id
        LEFT JOIN Directs dir ON m.Movie_ID = dir.Movie_id
        LEFT JOIN Contributors d ON dir.Contributor_id = d.contributor_id
        LEFT JOIN Rate r ON m.Movie_ID = r.Movie_ID
        LEFT JOIN Make mk ON m.Movie_ID = mk.Movie_id
        LEFT JOIN Studio s ON mk.Studio_id = s.studio_id
        LEFT JOIN Is_Genre ig ON m.Movie_ID = ig.Movie_id
        LEFT JOIN Genre g ON ig.Genre_id = g.genre_id
        WHERE {where_clause}
        GROUP BY m.Movie_ID, c.first_name, c.last_name, d.first_name, d.last_name, m.length, m.MPA_RATING
        ORDER BY {sort_columns[sort_field]} {sort_order_sql}, m.title ASC
    """
    try:
        cursor.execute(sql_query, (f"%{search_query}%",))
        movies = cursor.fetchall()
        return movies  # It's usually better to return the data and print it outside the function
    except Exception as e:  # It's better to capture a more specific exception if possible
        print(f"An error occurred: {e}")
        return None


def add_movie(args, cursor):
    try:
        cursor.execute('''INSERT INTO movie(movie_id, length, title, mpa_rating)
            VALUES(0, 'P0000-00-00T02:04:00', 'Sausage Party', 'R')''')
    except psycopg2.Error as e:
        print(f"Error: {e} {cursor.statusmessage}")

def add_movie_to_collection(conn, collection_id, name):
    cursor = conn.cursor()
    try:
        cursor.execute(
            "Insert into collection(collection_id, name) VALUES (%s, %s)",
            (collection_id, name)
        )
        conn.commit()
        print(f"Movie added to collection successfully.")
    except psycopg2.Error as e:
        print(f"An error occurred: {e}")
        conn.rollback()

def delete_movie_from_collection(conn, collection_id, name):
    cursor = conn.cursor()
    try:
        cursor.execute(
            "DELETE FROM collection WHERE collection_id = %s AND name = %s",
            (collection_id, name)
        )
        conn.commit()
        print(f"Movie removed from collection successfully.")
    except psycopg2.Error as e:
        print(f"An error occurred: {e}")
        conn.rollback()

def modify_collection_name(conn, collection_id, name):
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE collection SET name = %s WHERE collection_id = %s",
            (name, collection_id)
        )
        conn.commit()
        print(f"Collection name updated successfully.")
    except psycopg2.Error as e:
        print(f"An error occurred: {e}")
        conn.rollback()

def delete_collection(conn, collection_id):
    cursor = conn.cursor()
    try:
        cursor.execute(
            "DELETE FROM collection WHERE collection_id = %s",
            (collection_id,)
        )
        conn.commit()
        print(f"Collection deleted successfully.")
    except psycopg2.Error as e:
        print(f"An error occurred: {e}")
        conn.rollback()

# TODO: Make sure movie ID is not referenced on 'available_on' table
def delete_movie(conn, movie_id):
    cursor = conn.cursor()
    try:
        cursor.execute('''DELETE FROM movie WHERE movie_id=%s''', (movie_id))
        conn.commit()
        print(f"Deleted movie.")
    except psycopg2.Error as e:
        print(f"Error: {e} {cursor.statusmessage}")

def rate_movie(conn, user_id, movie_id, star_rating):
    cursor = conn.cursor()
    try:
        cursor.execute('''Insert into Rate(user_id, movie_id, star_rating)
            Values(%s, %s, %s)''', (user_id, movie_id, star_rating)) 
        conn.commit()
        print(f"Rated movie.")
    except psycopg2.Error as e:
        print(f"Error: {e} {cursor.statusmessage}")

def watch_movie(conn, user_id, movie_id):
    cursor = conn.cursor()
    date_time = datetime.now()
    try:
        cursor.execute('''Insert into watch_movie(user_id, movie_id, date_time)
            Values(%s, %s, %s)''', (user_id, movie_id, date_time))
        conn.commit()
        print(f"Watched movie with ID: {movie_id[0]}.")
    except psycopg2.Error as e:
        print(f"Error: {e} {cursor.statusmessage}")

# "INSERT INTO Collection (Collection_ID, name) VALUES (%s, %s)",
#             (user_id, collection_name)

def watch_collection(conn, user_id, collection_id):
    cursor = conn.cursor()
    play_time = datetime.now()
    try:
        # Retrieve all movies in the collection
        cursor.execute(
            ''' 
            select m.movie_id
            from collection c
            join holds h on c.collection_id = h.collection_id
            join movie m on m.movie_id=h.movie_id
            join users u on u.user_id=c.user_id
            where u.user_id=4
            group by c.name, m.movie_id
            '''
        )
        movies = cursor.fetchall()
        
        # Record the play for each movie in the collection
        for movie in movies:
            watch_movie(conn, user_id, movie)  # Assuming the movie_id is the first element in the tuple

        print(f"Collection with ID {collection_id} was played by user {user_id}.")
    except psycopg2.Error as e:
        print(f"An error occurred while playing the collection: {e}")
        conn.rollback()

def follow_user(conn, follower_id, followee_id):
    cursor = conn.cursor()
    try:
        cursor.execute('''Insert into following(follower_id, followee_id)
            Values(%s, %s)''', (followee_id, followee_id))
        conn.commit()
        print(f"Followed user.")
    except psycopg2.Error as e:
        print(f"Error: {e} {cursor.statusmessage}")

def unfollow_user(conn, follower_id):
    cursor = conn.cursor()
    try:
        cursor.execute('''DELETE FROM following WHERE follower_id=%s''', (follower_id,))
        conn.commit()
        print(f"Unfollowed user.")
    except psycopg2.Error as e:
        print(f"Error: {e} {cursor.statusmessage}")

def search_users(conn, email):
    cursor = conn.cursor()
    try:
        cursor.execute('''SELECT * FROM Users WHERE email=%s''', (email,))
        conn.commit()
        users = cursor.fetchall()
        for user in users:
            print(f"{user}")
        print(f"Searched users")
    except psycopg2.Error as e:
        print(f"Error: {e} {cursor.statusmessage}")