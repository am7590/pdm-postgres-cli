import argparse
import psycopg2
import paramiko
from sshtunnel import SSHTunnelForwarder
from setup import *
from datetime import datetime
from getpass import getpass
import uuid

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

def add_movie_to_collection(conn, collection_id, movie_id):
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO collection_movies (collection_id, movie_id) VALUES (%s, %s)",
            (collection_id, movie_id)
        )
        conn.commit()
        print(f"Movie added to collection successfully.")
    except psycopg2.Error as e:
        print(f"An error occurred: {e}")
        conn.rollback()

def delete_movie_from_collection(conn, collection_id, movie_id):
    cursor = conn.cursor()
    try:
        cursor.execute(
            "DELETE FROM collection_movies WHERE collection_id = %s AND movie_id = %s",
            (collection_id, movie_id)
        )
        conn.commit()
        print(f"Movie removed from collection successfully.")
    except psycopg2.Error as e:
        print(f"An error occurred: {e}")
        conn.rollback()

def modify_collection_name(conn, collection_id, new_name):
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE collections SET collection_name = %s WHERE collection_id = %s",
            (new_name, collection_id)
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
            "DELETE FROM collections WHERE collection_id = %s",
            (collection_id,)
        )
        conn.commit()
        print(f"Collection deleted successfully.")
    except psycopg2.Error as e:
        print(f"An error occurred: {e}")
        conn.rollback()


# TODO: Make sure movie ID is not referenced on 'available_on' table
def delete_movie(args, cursor):
    try:
        cursor.execute('''DELETE FROM p320_12.p320_12.movie WHERE movie_id=0''')
    except psycopg2.Error as e:
        print(f"Error: {e} {cursor.statusmessage}")

def rate_movie(args, cursor):
    try:
        cursor.execute('''Insert into Rate(user_id, movie_id, star_rating)
            Values(1, 2, 4.8)''')
    except psycopg2.Error as e:
        print(f"Error: {e} {cursor.statusmessage}")

def watch_movie(args, cursor):
    try:
        cursor.execute('''Insert into watch_movie(user_id, movie_id, date_time)
            Values(1, 4, '2019-06-20 6:45:00')''')
    except psycopg2.Error as e:
        print(f"Error: {e} {cursor.statusmessage}")

def follow_user(args, cursor):
    try:
        cursor.execute('''Insert into following(follower_id, followee_id)
            Values(1, 1)''')
    except psycopg2.Error as e:
        print(f"Error: {e} {cursor.statusmessage}")


def unfollow_user(args, cursor):
    try:
        cursor.execute('''DELETE FROM following WHERE follower_id=1''')
    except psycopg2.Error as e:
        print(f"Error: {e} {cursor.statusmessage}")



def run_cli():
    with SSHTunnelForwarder(
        ssh_config["ssh_address_or_host"],
        ssh_username=ssh_config["ssh_username"],
        ssh_password=ssh_config["ssh_password"],
        remote_bind_address=("127.0.0.1", 5432),
        local_bind_address=("0.0.0.0", 5432),
        ssh_port=ssh_config["ssh_port"],
    ) as tunnel:
        connection = psycopg2.connect(
            database=db_params["database"],
            user=db_params["user"],
            password=db_params["password"],
            host=db_params["host"],
            port=tunnel.local_bind_port,
        )

        cursor = connection.cursor()
        parser = argparse.ArgumentParser(description="User Management System")
        subparsers = parser.add_subparsers(dest='action')

        # db_subparsers = parser.add_subparsers(÷dest='action')
        ''' 
        Users will be able to create new accounts and access via login. The system must record
        the date and time an account is created. It must also store the dates and times users
        access the application
        '''
        create_user_parser = subparsers.add_parser("create_user", help="Create a new user")

        '''
        Users will be able to create collections of movies.
        '''
        create_collections_parser = subparsers.add_parser("create_collection", help="Create a new collection")

        '''
        Users will be to see the list of all their collections by name in ascending order. The list
        must show the collection name, number of movies in the collection, and total length of the 
        movies (in hours:minutes) of movies in the collection
        '''
        list_collections_parser = subparsers.add_parser("list_collections", help="List all movie collections")

        '''
        Users will be able to search for movies by name, release date, cast members, studio, or
        genre. The resulting list of movies must show the movie’s name, the cast members, the
        director, the length and the ratings (MPAA and user). The list must be sorted alpha-
        betically (ascending) by movie’s name and release date. Users can sort the resulting
        list by: movie name, studio, genre, and released year (ascending and descending).
        '''
        search_movies_parser = subparsers.add_parser("search_movies", help="Search for movies")

        # add_movie
        add_movie_parser = subparsers.add_parser("add_movie", help="Add a movie to a collection")

        # delete_movie
        delete_movie_parser = subparsers.add_parser("delete_movie", help="Delete a movie from a collection")

        # Modify the name of a collection, delete an entire collection

        # rate_movie
        rate_movie_parser = subparsers.add_parser("rate_movie", help="Rate a movie")

        # watch_movie (individual or entire collection)
        watch_movie_parser = subparsers.add_parser("watch_movie", help="Watch a movie")

        # follow_user (by email)
        follow_user_parser = subparsers.add_parser("follow_user", help="Follow a user")

        # unfollow_user
        unfollow_user_parser = subparsers.add_parser("unfollow_user", help="Unfollow a user")

        # Subparser for creating a user
        create_user_parser.add_argument('username', type=str, help='Enter your username')
        create_user_parser.add_argument('password', type=str, help='Enter your password')
        create_user_parser.add_argument('email', type=str, help='Enter your email')
        create_user_parser.add_argument('first_name', type=str, help='Enter your first name')
        create_user_parser.add_argument('last_name', type=str, help='Enter your last name')

        create_collections_parser.add_argument('user_id', type=int, help='Your user ID to create collections')
        create_collections_parser.add_argument('collection_name', type=str, help='Your collection\'s name')

        # Subparser for listing collections
        list_collections_parser.add_argument('user_id', type=int, help='Your user ID to list collections')

        # Subparser for searching movies
        search_movies_parser.add_argument('search_query', type=str, help='Query to search for movies')

        # Subparser for adding a movie
        add_movie_parser.add_argument('collection_id', type=int, help='ID of the collection to add the movie to')
        add_movie_parser.add_argument('movie_id', type=int, help='ID of the movie to add to the collection')

        # Subparser for deleting a movie
        delete_movie_parser.add_argument('movie_id', type=int, help='ID of the movie to delete')

        # Subparser for rating a movie
        rate_movie_parser.add_argument('user_id', type=int, help='Your user ID to rate a movie')
        rate_movie_parser.add_argument('movie_id', type=int, help='ID of the movie to rate')
        rate_movie_parser.add_argument('star_rating', type=float, help='Your rating for the movie')

        # Subparser for watching a movie
        watch_movie_parser.add_argument('user_id', type=int, help='Your user ID to register the movie as watched')
        watch_movie_parser.add_argument('movie_id', type=int, help='ID of the movie you watched')

        # Subparser for following a user
        follow_user_parser.add_argument('follower_id', type=int, help='Your user ID to follow someone')
        follow_user_parser.add_argument('followee_id', type=int, help='User ID of the person you want to follow')

        # Subparser for unfollowing a user
        unfollow_user_parser.add_argument('follower_id', type=int, help='Your user ID to unfollow someone')


        # create_user_parser.set_defaults(dest=create_user)
        create_collections_parser.set_defaults(dest=create_collection)
        list_collections_parser.set_defaults(dest=list_collections)
        search_movies_parser.set_defaults(dest=search_movies)
        add_movie_parser.set_defaults(dest=add_movie)
        delete_movie_parser.set_defaults(dest=delete_movie)
        rate_movie_parser.set_defaults(dest=rate_movie)
        watch_movie_parser.set_defaults(dest=watch_movie)
        follow_user_parser.set_defaults(dest=follow_user)
        unfollow_user_parser.set_defaults(dest=unfollow_user)

        args = parser.parse_args()

        # Handle authentication actions
        if args.action == 'create':
            create_user(connection, args.username, args.password, args.email, args.first_name, args.last_name)
        elif args.action == 'login':
            login_user(connection, args.username, args.password)
        elif args.action == 'create_collection':
            create_collection(connection, args.user_id, args.collection_name)
        elif args.action == 'list_collections':
            list_collections(connection, args.user_id)
        elif args.action == 'search_movies':
            search_movies(connection, args.search_query)
        elif args.action == 'add_movie':
            add_movie(connection, args.collection_id, args.movie_id)
        elif args.action == 'delete_movie':
            delete_movie(connection, args.movie_id)
        elif args.action == 'rate_movie':
            rate_movie(connection, args.user_id, args.movie_id, args.star_rating)
        elif args.action == 'watch_movie':
            watch_movie(connection, args.user_id, args.movie_id)
        elif args.action == 'follow_user':
            follow_user(connection, args.follower_id, args.followee_id)
        elif args.action == 'unfollow_user':
            unfollow_user(connection, args.follower_id)
        else:
            parser.print_help()
            connection.close()

if __name__ == "__main__":
    run_cli()

# Database connection function with SSH tunneling
# def connect_to_database():
    

        # Perform database operations here
        # cursor.execute("SELECT version()")
        # version = cursor.fetchone()
        # print("PostgreSQL version:", version)
        # parser = argparse.ArgumentParser(description="Movie Collection CLI")
        # subparsers = parser.add_subparsers(title="Subcommands", dest="subcommand")

        # args = parser.parse_args()

        # Connect to the database
        # if hasattr(args, "func"):
        #     if conn is not None:
        #         args.func(args, cursor)
        #         conn.commit()
        #         conn.close()
        #     else:
        #         print("Unable to connect to the database via SSH tunnel. Please check your SSH and database credentials.")
        # else:
            # print("No subcommand specified. Use --help for usage instructions.")
            # print("Welcome to Movies Database. Type in your username:")
