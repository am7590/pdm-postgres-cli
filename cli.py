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
    
# Auto increment ID
# create_user(connection, args.username, args.password, args.email, args.first_name, args.last_name)
def create_user(conn, username, password, email, first_name, last_name):
    cursor = conn.cursor()
    try:
        # We no longer need to manually set `user_id`, assuming it is auto-incremented by the database.
        last_access_date = datetime.now()
        creation_date = datetime.now()
        print("inserting")
        # Use a parameterized query for safety and correctness.
        cursor.execute(
            "INSERT INTO Users (user_id, last_access_date, creation_date, username, passwordhash, email, first_name, lastname) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (100000, last_access_date, creation_date, username, password, email, first_name, last_name)
        )
        conn.commit()
        print(f"Successfully created user {username}")
    except psycopg2.Error as e:
        # In case of an exception, print the error message from psycopg2
        print(f"An error occurred: {e}")
        conn.rollback()
        # Function to create a new user
# def create_user(conn, username, password, email, first_name, last_name):
#     creation_date = datetime.now()
#     cursor = conn.cursor()
#     try:
#         cursor.execute(
#             "INSERT INTO users (username, password, email, first_name, last_name, creation_date, last_access_date) "
#             "VALUES (%s, %s, %s, %s, %s, %s, %s)",
#             (username, password, email, first_name, last_name, creation_date, creation_date)
#         )
#         conn.commit()
#         print(f"Account created for {username} on {creation_date}")
#     except psycopg2.Error as e:
#         print(f"An error occurred: {e}")
#         conn.rollback()
#     finally:
#         cursor.close()

# TODO: Fetch all collections
def list_collections(args, cursor):
    try:
        cursor.execute("SELECT * FROM Users")

        collections = cursor.fetchall()

        if collections:
            print("User Collection:")
            for collection in collections:
                print(f"{collection}")
        else:
            print("No movie collections found.")

        cursor.close()
    except psycopg2.Error as e:
        print(f"Error listing collections: {e}")
        

def search_movies(args, cursor):
    try:
        cursor.execute("SELECT * FROM Movie")

        collections = cursor.fetchall()

        if collections:
            print("Movie Collection:")
            for collection in collections:
                print(f"{collection}")
        else:
            print("No movie collections found.")

        cursor.close()
    except psycopg2.Error as e:
        print(f"Error listing collections: {e}")


def add_movie(args, cursor):
    try:
        cursor.execute('''INSERT INTO movie(movie_id, length, title, mpa_rating)
            VALUES(0, 'P0000-00-00T02:04:00', 'Sausage Party', 'R')''')
    except psycopg2.Error as e:
        print(f"Error: {e} {cursor.statusmessage}")

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

        # Subparser for creating a user
        parser_create = subparsers.add_parser('create', help='Create a new user account')
        parser_create.add_argument('username', type=str, help='Username for the new account')
        parser_create.add_argument('password', type=str, help='Password for the new account')
        parser_create.add_argument('email', type=str, help='Email address for the new account')
        parser_create.add_argument('first_name', type=str, help='First name of the user')
        parser_create.add_argument('last_name', type=str, help='Last name of the user')

        # Subparser for logging in
        parser_login = subparsers.add_parser('login', help='Log into the system')
        parser_login.add_argument('username', type=str, help='Your username')
        parser_login.add_argument('password', type=str, help='Your password')

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

        # create_user_parser.set_defaults(dest=create_user)
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
        elif args.action == 'list_collections':
            list_collections(connection, cursor)
            print("listing collections")
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
