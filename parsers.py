import argparse
import psycopg2
from helpers import *


parser = argparse.ArgumentParser(description="User Management System")
subparsers = parser.add_subparsers(dest='action')

# Create account, login
create_user_parser = subparsers.add_parser("create_user", help="Create a new user")
login_user_parser = subparsers.add_parser("login", help="Login user")

# Create collections
create_collections_parser = subparsers.add_parser("create_collection", help="Create a new collection")

# List a user's collections by name in ascending oder. 
# The list must show the collection name, number of movies in the collection, and total length of the 
#     movies (in hours:minutes) of movies in the collection
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

# Add/delete from connection
add_movie_to_collection_parser = subparsers.add_parser("add_movie_to_collection", help="Add a movie to a user's collection")
delete_movie_from_collection_parser = subparsers.add_parser("delete_movie_from_collection", help="Delete a movie to a user's collection")

# delete_movie
delete_movie_parser = subparsers.add_parser("delete_movie", help="Delete a movie from a collection")

# Modify the name of a collection, delete an entire collection
modify_collection_name_parser = subparsers.add_parser("modify_collection_name", help="Modify a collection")
delete_collection_parser = subparsers.add_parser("delete_collection", help="Delete a collection")

# rate_movie
rate_movie_parser = subparsers.add_parser("rate_movie", help="Rate a movie")

# watch_movie (individual or entire collection)
watch_movie_parser = subparsers.add_parser("watch_movie", help="Watch a movie")
watch_collection_parser = subparsers.add_parser("watch_collection", help="Watch a collection")

# follow_user (by email)
follow_user_parser = subparsers.add_parser("follow_user", help="Follow a user")

# unfollow_user
unfollow_user_parser = subparsers.add_parser("unfollow_user", help="Unfollow a user")

search_users_parser = subparsers.add_parser("search_users", help="Search a user via email")

#  creating a user
create_user_parser.add_argument('username', type=str, help='Enter your username')
create_user_parser.add_argument('password', type=str, help='Enter your password')
create_user_parser.add_argument('email', type=str, help='Enter your email')
create_user_parser.add_argument('first_name', type=str, help='Enter your first name')
create_user_parser.add_argument('last_name', type=str, help='Enter your last name')

# login
login_user_parser.add_argument('username', type=str, help='Enter your username')
login_user_parser.add_argument('password', type=str, help='Enter your password')

create_collections_parser.add_argument('user_id', type=int, help='Your user ID to create collections')
create_collections_parser.add_argument('collection_name', type=str, help='Your collection\'s name')

# Subparser for listing collections
list_collections_parser.add_argument('user_id', type=int, help='Your user ID to list collections')

# Subparser for searching movies (search_field, search_query, sort_field, sort_order)
search_movies_parser.add_argument('search_field', type=str, help='Field to search for movies')
search_movies_parser.add_argument('search_query', type=str, help='Query to search for movies')
search_movies_parser.add_argument('sort_field', type=str, help='Sort option')
search_movies_parser.add_argument('sort_order', type=str, help='Sort order')

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

watch_collection_parser.add_argument('user_id', type=int, help='Your user ID to register the movies as watched')
watch_collection_parser.add_argument('collection_id', type=int, help='ID of the collection you want to watch')

# Subparser for following a user
follow_user_parser.add_argument('follower_id', type=int, help='Your user ID to follow someone')
follow_user_parser.add_argument('followee_id', type=int, help='User ID of the person you want to follow')

# Subparser for unfollowing a user
unfollow_user_parser.add_argument('follower_id', type=int, help='Your user ID to unfollow someone')

# add movie to collection
add_movie_to_collection_parser.add_argument('collection_id', type=int, help="The collection's ID")
add_movie_to_collection_parser.add_argument('name', type=str, help="The collection's name")

# delete movie from collection
delete_movie_from_collection_parser.add_argument('collection_id', type=int, help="The collection's ID")
delete_movie_from_collection_parser.add_argument('name', type=str, help="The collection's name")

# modify collection name
modify_collection_name_parser.add_argument('collection_id', type=int, help="The collection's ID")
modify_collection_name_parser.add_argument('name', type=str, help="The collection's name")

# delete collection
delete_collection_parser.add_argument('collection_id', type=int, help="The collection's ID")

# search users (by email)
search_users_parser.add_argument('email', type=str, help="The user's email to search")

# Set default functions for parsers
create_user_parser.set_defaults(dest=create_user)
login_user_parser.set_defaults(dest=login_user)
create_collections_parser.set_defaults(dest=create_collection)
list_collections_parser.set_defaults(dest=list_collections)
add_movie_to_collection_parser.set_defaults(dest=add_movie_to_collection)
delete_movie_from_collection_parser.set_defaults(dest=delete_movie_from_collection)
modify_collection_name_parser.set_defaults(dest=modify_collection_name)
delete_collection_parser.set_defaults(dest=delete_collection)
search_movies_parser.set_defaults(dest=search_movies)
add_movie_parser.set_defaults(dest=add_movie)
delete_movie_parser.set_defaults(dest=delete_movie)
rate_movie_parser.set_defaults(dest=rate_movie)
watch_movie_parser.set_defaults(dest=watch_movie)
watch_collection_parser.set_defaults(dest=watch_collection)
follow_user_parser.set_defaults(dest=follow_user)
unfollow_user_parser.set_defaults(dest=unfollow_user)
search_users_parser.set_defaults(dest=search_users)