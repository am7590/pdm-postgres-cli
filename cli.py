import argparse
import psycopg2
import paramiko
from sshtunnel import SSHTunnelForwarder
from setup import *

# Database connection function with SSH tunneling
def connect_to_database():
    with SSHTunnelForwarder(
        ssh_config["ssh_address_or_host"],
        ssh_username=ssh_config["ssh_username"],
        ssh_password=ssh_config["ssh_password"],
        remote_bind_address=("127.0.0.1", 5432),
        local_bind_address=("0.0.0.0", 5432),
        ssh_port=ssh_config["ssh_port"],
    ) as tunnel:
        conn = psycopg2.connect(
            database=db_params["database"],
            user=db_params["user"],
            password=db_params["password"],
            host=db_params["host"],
            port=tunnel.local_bind_port,
        )

        cursor = conn.cursor()
        # Perform database operations here
        cursor.execute("SELECT version()")
        version = cursor.fetchone()
        print("PostgreSQL version:", version)

        args = parser.parse_args()

        # Connect to the database
        if hasattr(args, "func"):
            if conn is not None:
                args.func(args, cursor)
                conn.close()
            else:
                print("Unable to connect to the database via SSH tunnel. Please check your SSH and database credentials.")
        else:
            print("No subcommand specified. Use --help for usage instructions.")


parser = argparse.ArgumentParser(description="Movie Collection CLI")
subparsers = parser.add_subparsers(title="Subcommands", dest="subcommand")

# list_collections
list_collections_parser = subparsers.add_parser("list_collections", help="List all movie collections")

# search_movies
search_movies_parser = subparsers.add_parser("search_movies", help="Search for movies")

# add_movie
add_movie_parser = subparsers.add_parser("add_movie", help="Add a movie to a collection")

# delete_movie
delete_movie_parser = subparsers.add_parser("delete_movie", help="Delete a movie from a collection")

# rate_movie
rate_movie_parser = subparsers.add_parser("rate_movie", help="Rate a movie")

# watch_movie
watch_movie_parser = subparsers.add_parser("watch_movie", help="Watch a movie")

# follow_user
follow_user_parser = subparsers.add_parser("follow_user", help="Follow a user")

# unfollow_user
unfollow_user_parser = subparsers.add_parser("unfollow_user", help="Unfollow a user")

# TODO: Fetch all collections
def list_collections(args, cursor):
    try:
        cursor.execute("SELECT * FROM Genre")

        collections = cursor.fetchall()

        if collections:
            print("Genra Collection:")
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

def add_movie(args):
    print("adding movie")
    # TODO
    pass

def delete_movie(args):
    print("deleting movie")
    # TODO
    pass

def rate_movie(args):
    print("rating movie")
    # TODO
    pass

def watch_movie(args):
    print("watching movie")
    # TODO
    pass

def follow_user(args):
    print("following user")
    # TODO
    pass

def unfollow_user(args):
    print("unfollowing user")
    # TODO
    pass

list_collections_parser.set_defaults(func=list_collections)
search_movies_parser.set_defaults(func=search_movies)
add_movie_parser.set_defaults(func=add_movie)
delete_movie_parser.set_defaults(func=delete_movie)
rate_movie_parser.set_defaults(func=rate_movie)
watch_movie_parser.set_defaults(func=watch_movie)
follow_user_parser.set_defaults(func=follow_user)
unfollow_user_parser.set_defaults(func=unfollow_user)


if __name__ == "__main__":
    connect_to_database()