import argparse
import psycopg2
import paramiko
from sshtunnel import SSHTunnelForwarder
from datetime import datetime
import uuid

from setup import *
from parsers import *

def run_cli():
    # Connect to DB
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

        # Create CLI; access helpers.py and parsers.py
        cursor = connection.cursor()
        args = parser.parse_args()

        # Handle user actions
        if args.action == 'create':
            create_user(connection, args.username, args.password, args.email, args.first_name, args.last_name)
        elif args.action == 'login':
            login_user(connection, args.username, args.password)
        elif args.action == 'create_collection':
            create_collection(connection, args.user_id, args.collection_name)
        elif args.action == 'list_collections':
            list_collections(connection, args.user_id)
        elif args.action == 'add_movie_to_collection':
            add_movie_to_collection(connection, args.collection_id, args.name)
        elif args.action == 'delete_movie_from_collection':
            delete_movie_from_collection(connection, args.collection_id, args.name)
        elif args.action == 'modify_collection_name':
            modify_collection_name(connection, args.collection_id, args.name)
        elif args.action == 'delete_collection':
            delete_collection(connection, args.collection_id)
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
        elif args.action == 'search_users':
            search_users(connection, args.email)
        else:
            parser.print_help()
            connection.close()

if __name__ == "__main__":
    run_cli()