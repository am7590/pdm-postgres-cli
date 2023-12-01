# Import functions to fetch user information
import time

from helpers import get_owned_collections, get_followers, get_following, get_top10_plays, get_top10_rating, \
    get_user_id, get_movie_title
import os

username = 0
user_id = 0
collections = 0
followers = 0
following = 0


def display_menu():
    os.system("clear")
    print("******************************************")
    print("********      User Profile      **********")
    print("******************************************")
    print(f"Currently Viewing User: {username}")
    print(f"\tCollections: {collections}")
    print(f"Followers: {followers}\t\tFollowing: {following}")
    print("\n")


def change_user(connection):
    global username
    global user_id
    global collections
    global followers
    global following
    os.system("clear")
    username = input("Enter the username of the profile you wish to view: ")
    user_id = get_user_id(connection, username)
    if user_id is None:
        print("User does not exist...")
        time.sleep(2)
        return change_user(connection)
    collections = get_owned_collections(connection, user_id)[0]
    followers = get_followers(connection, user_id)[0]
    following = get_following(connection, user_id)[0]


def show_t10_plays(connection):
    print(f"{username}'s Top 10 movies by plays:")
    top = get_top10_plays(connection, user_id)
    idx = 1
    for movie in top:
        title = get_movie_title(connection, movie[0])
        print(f"{idx}.\t{title}\n\tPlays: {movie[1]}\n")
        idx += 1
    input("Press enter to return to menu...")


def show_t10_rating(connection):
    print(f"{username}'s Top 10 movies by rating:")
    top = get_top10_rating(connection, user_id)
    idx = 1
    for movie in top:
        title = get_movie_title(connection, movie[0])
        print(f"{idx}.\t{title}\n\tRating: {movie[1]:.2f}\n")
        idx += 1
    input("Press enter to return to menu...")


def user_profile_menu(connection):
    change_user(connection)

    while True:
        display_menu()
        print("Select an option:")
        print(f"1. Show {username}'s Top 10 movies by plays")
        print(f"2. Show {username}'s Top 10 movies by rating")
        print("3. Change user")
        print("4. Exit")
        choice = input("Enter your choice: ")
        
        if choice == "1":
            show_t10_plays(connection)
        elif choice == "2":
            show_t10_rating(connection)
        elif choice == "3":
            change_user(connection)
        elif choice == "4":
            break
        else:
            input("Invalid choice... Press enter to return to selection.")