from datetime import datetime

import psycopg2


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
        cursor.execute(
            "INSERT INTO Users (user_id, last_access_date, creation_date, username, passwordhash, email, first_name, last_name) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (22, last_access_date, creation_date, username, password, email, first_name, last_name)
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
            "INSERT INTO Collection (Collection_ID, name, user_id) VALUES (%s, %s, %s)",
            (user_id, collection_name, 1)
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

    if search_field == "name":
        search_by_name(conn, search_query)
    elif search_field == "studio":
        print("search by studio")
    elif search_field == "genre":
        print("Search by studio")
    elif search_field == "release":
        print("Search by release date")
        search_by_release_date(conn, search_query)
    
# python3 cli.py search_movies name Deadpool field order
def search_by_name(conn, movie_name):
    cursor = conn.cursor()
    try:
        # Basic info
        print("Basic info:")
        cursor.execute("""
            select  m.title,m.length, m.release_date, m.mpa_rating
            from movie m
            where m.title = %s;
        """, (movie_name,))
        movies = cursor.fetchall()
        for movie in movies:
            print(f"{movie}")
        print("\n")

        # Contributers
        print("Contributers and directors:")
        cursor.execute("""
            select ct.first_name,ct.last_name
            from contributors ct
            join acted_on ao on ct.contributor_id = ao.contributor_id
            join movie m on ao.movie_id = m.movie_id
            where m.title=%s;
        """, (movie_name,))
        movies = cursor.fetchall()
        for movie in movies:
            print(f"{movie}")
        print("\n")
        
    except psycopg2.Error as e:
        print(f"Error searching by movie name: {e}")

# python3 cli.py search_movies release 2019-04-26 field order
def search_by_release_date(conn, date):
    cursor = conn.cursor()
    try:
        cursor.execute("""
            select c.name,  sum(m.length) as total_length, m.title, m.release_date
            from collection c
            join holds h on c.collection_id = h.collection_id
            join movie m on m.movie_id=h.movie_id
            join users u on u.user_id=c.user_id
            where u.user_id=4 and m.release_date=%s
            group by c.name, m.movie_id
        """, (date,))
        movies = cursor.fetchall()
        for movie in movies:
            print(f"Movie: {movie}")
    except psycopg2.Error as e:
        print(f"Error searching by movie name: {e}")


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
            "Insert into holds(collection_id, movie_id) VALUES (%s, %s)",
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
            "DELETE FROM holds WHERE collection_id = %s AND movie_id = %s",
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
        print(f"Watched movie with ID: {movie_id}.")
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
            Values(%s, %s)''', (follower_id, followee_id))
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


#####################
###### Phase 3 ######
#####################

def top_twenty(conn, followee_id):
    curser = conn.cursor()
    try:
        cursor.execute('''
            select avg(r.star_rating) as average_rate, m.title as movie_title
            from following f
            join rate r on r.user_id=follower_id
            join movie m on m.movie_id=r.movie_id
            where f.followee_id=%s
            group by movie_title
            order by average_rate DESC
            limit 20;
        ''', (followee_id,))
        conn.commit()
        movies = curser.fetchall()
        for movie in movies:
            print(f"{movie}")
    except psycopg2.Error as e:
        print(f"Error: {e} {cursor.statusmessage}")

def top_five(conn):
    curser = conn.cursor()
    try:
        cursor.execute('''
            select r.movie_id, m.title,avg(star_rating) as average_rate from rate r
            join   p320_12.movie m on r.movie_id = m.movie_id
            where  m.release_date between '2023-04-01 00:00:00.000000' And '2023-04-30 00:00:00.000000'
            group by r.movie_id, m.title
            order by average_rate DESC
            LIMIT 5;
        ''')
        conn.commit()
        movies = curser.fetchall()
        for movie in movies:
            print(f"{movie}")
    except psycopg2.Error as e:
        print(f"Error: {e} {cursor.statusmessage}")

# TODO: pass in user_id?
def movies_based_on_genre_history(conn, genre):
    curser = conn.cursor()
    try:
        cursor.execute('''
            select  m.title, avg(star_rating) as average_rate from rate r
            join    movie m on m.movie_id=r.movie_id
            join    is_genre ig on m.movie_id=ig.movie_id
            join    genre g on g.genre_id=ig.genre_id
            where g.genre_name=%s
            group by m.title
            order by average_rate
            limit 5;
        ''', (genre,))
        conn.commit()
        movies = curser.fetchall()
        for movie in movies:
            print(f"{movie}")
    except psycopg2.Error as e:
        print(f"Error: {e} {cursor.statusmessage}")

def movies_based_on_cast_history(conn, cast_name):
    curser = conn.cursor()
    try:
        cursor.execute('''
            select  m.title, avg(star_rating) as average_rate from rate r
            join    movie m on m.movie_id=r.movie_id
            join    acted_on ao on m.movie_id = ao.movie_id
            join    contributors c on ao.contributor_id=c.contributor_id
            where c.first_name='Chris'
            group by m.title
            order by average_rate
            limit 10;
        ''', (cast_name,))
        conn.commit()
        movies = curser.fetchall()
        for movie in movies:
            print(f"{movie}")
    except psycopg2.Error as e:
        print(f"Error: {e} {cursor.statusmessage}")

def movies_based_on_mpaa(conn, rating):
    curser = conn.cursor()
    try:
        cursor.execute('''
            select  m.title, avg(star_rating) as average_rate from rate r
            join    movie m on m.movie_id=r.movie_id
            where m.mpa_rating=%s
            group by m.title
            order by average_rate DESC
            limit 10;
        ''', (rating,))
        conn.commit()
        movies = curser.fetchall()
        for movie in movies:
            print(f"{movie}")
    except psycopg2.Error as e:
        print(f"Error: {e} {cursor.statusmessage}")

# TODO: Pass in user_id
def movies_based_on_star_rating(conn):
    curser = conn.cursor()
    try:
        cursor.execute('''
            select  m.title, avg(star_rating) as average_rate from rate r
            join    movie m on m.movie_id=r.movie_id
            group by m.title
            order by average_rate DESC
            limit 10;
        ''', (rating,))
        conn.commit()
        movies = curser.fetchall()
        for movie in movies:
            print(f"{movie}")
    except psycopg2.Error as e:
        print(f"Error: {e} {cursor.statusmessage}")


def get_user_id(conn, username):
    cursor = conn.cursor()
    try:
        cursor.execute("""
                    SELECT user_id
                    FROM users
                    WHERE username = %s;
                    """, [username])
        return cursor.fetchone()
    except psycopg2.Error as e:
        print(f"Error listing collections: {e}")


def get_owned_collections(conn, user_id):
    cursor = conn.cursor()
    try:
        cursor.execute("""
                SELECT COUNT(*) AS user_id_count
                FROM collection
                WHERE user_id = %s;
                """, [user_id])
        return cursor.fetchone()
    except psycopg2.Error as e:
        print(f"Error listing collections: {e}")


def get_followers(conn, user_id):
    cursor = conn.cursor()
    try:
        cursor.execute("""
                    SELECT COUNT(*) AS follower_id_count
                    FROM following
                    WHERE followee_id = %s;
                    """, [user_id])
        return cursor.fetchone()
    except psycopg2.Error as e:
        print(f"Error listing followers: {e}")


def get_following(conn, user_id):
    cursor = conn.cursor()
    try:
        cursor.execute("""
                    SELECT COUNT(*) AS followee_id_count
                    FROM following
                    WHERE follower_id = %s;
                    """, [user_id])
        return cursor.fetchone()
    except psycopg2.Error as e:
        print(f"Error listing followers: {e}")


def get_top10_rating(conn, user_id):
    cursor = conn.cursor()
    try:
        cursor.execute("""
                    SELECT movie_id, AVG(star_rating) AS avg_rating
                    FROM rate
                    WHERE user_id = 1
                    GROUP BY movie_id
                    ORDER BY avg_rating DESC
                    LIMIT 10;
                        """, [user_id])
        return cursor.fetchall()
    except psycopg2.Error as e:
        print(f"Error: {e}")


def get_top10_plays(conn, user_id):
    cursor = conn.cursor()
    try:
        cursor.execute("""
                    SELECT movie_id, COUNT(*) AS frequency
                    FROM watch_movie
                    WHERE user_id = %s
                    GROUP BY movie_id
                    ORDER BY frequency DESC
                    LIMIT 10;
                            """, [user_id])
        return cursor.fetchall()
    except psycopg2.Error as e:
        print(f"Error: {e}")


def get_movie_title(conn, movie_id):
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT title FROM movie WHERE movie_id = %s", [movie_id])
        return cursor.fetchone()[0]
    except psycopg2.Error as e:
        print(f"Error fetching movie title: {e}")
