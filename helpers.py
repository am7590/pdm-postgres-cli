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

# TODO: finish this
'''
- [ ] Users will be to see the list of all their collections by name in ascending order. The list must show the following information per collection:
    - [ ] Collection’s name
    - [ ] # of movies in the collection
    - [ ] Total length of movies (hours:minutes) in the collection
'''
def list_collections(conn, user_id):
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT * FROM Collection
            """)
        collections = cursor.fetchall()
        for collection_name, movie_count, total_length in collections:
            print(f"Collection: {collection_name}, Movies: {movie_count}, Total Length: {str(total_length)}")
    except psycopg2.Error as e:
        print(f"Error listing collections: {e}") 

def search_movies(conn, search_query):
    cursor = conn.cursor()
    # Assuming there's a full-text search index or some logic to search based on the given query
    try:
        cursor.execute("""
            SELECT m.title, array_agg(a.name), d.name, m.length, m.mpaa_rating, AVG(r.star_rating)
            FROM movies m
            JOIN cast_members cm ON m.movie_id = cm.movie_id
            JOIN actors a ON cm.actor_id = a.actor_id
            JOIN directors d ON m.director_id = d.director_id
            LEFT JOIN ratings r ON m.movie_id = r.movie_id
            WHERE m.title LIKE %s OR a.name LIKE %s OR d.name LIKE %s -- and so on for other fields
            GROUP BY m.title, d.name, m.length, m.mpaa_rating
            ORDER BY m.title ASC, m.release_date ASC
            """, (f"%{search_query}%", f"%{search_query}%", f"%{search_query}%"))
        movies = cursor.fetchall()
        for movie in movies:
            print(f"Movie: {movie}")
    except psycopg2.Error as e:
        print(f"Error searching movies: {e}")

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
        print(f"Watched movie.")
    except psycopg2.Error as e:
        print(f"Error: {e} {cursor.statusmessage}")

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