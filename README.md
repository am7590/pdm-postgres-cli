# pdm-postgres-cli

## Setting up
- Clone the repo
- Create a 'database_credentials.txt' file in the same directory
- Add the following information to 'database_credentials.txt':
  ```
    DB_USER=...
    DB_PASSWORD=...
  ```
- Do NOT commit this file! You can create a .gitignore containing the following:
  ```
    # .gitignore

    # Database credentials
    database_credentials.txt
  ```
## For the presentation (follow this step by step):
- Users will be able to create new accounts and access via login. The system must record
the date and time an account is created. It must also store the dates and times users
access the application
  - Show in DataGrip: ```select * from users```
  - Create a new account: ```python3 cli.py create_user username2 password2 email2@gmail.com first last```
  - Show in DataGrip: ```select * from users```
  - Login: ``` python3 cli.py login am7590 am7590 ```
  - Show in DataGrip: ```select * from users```

- Users will be able to create collections of movies.
  - Show in DataGrip: ```select * from collection```
  - Create collection: ```python3 cli.py create_collection 12 my_other_other_collection```
  - Show in DataGrip: ```select * from collection```

- Users can modify the name of a collection. They can also delete an entire collection
  - Show in DataGrip: ```select * from collection```
  - Modify a collection: ```python3 cli.py modify_collection_name 12 good```
  - Show in DataGrip: ```select * from collection```
  - Delete collection: ```python3 cli.py delete_collection 12```

- Users will be to see the list of all their collections by name in ascending order and show collection name, # of movies in the collection, and the total length of the movies
  - List collections: ```python3 cli.py list_collections 1```

- Users will be able to search for movies by name, release date, cast members, studio, or
genre. Must show the movie's name, release data, cast members, director, length, and ratings.
  - Search: ```python3 cli.py search_movies name Deadpool default default```

- Users can add and delete movies from their collection (holds represents movies in collections)
  - Show in DataGrip: ```select * from holds```
  - Delete from collection: ```python3 cli.py delete_movie_from_collection 11 20```
  - Show in DataGrip: ```select * from holds```
  - Add to collection: ```python3 cli.py add_movie_to_collection 11 20```
  - Show in DataGrip: ```select * from holds```

- Users can rate a movie (star rating)
  - Show in DataGrip: ```select * from rate```
  - Rate a movie: ```python3 cli.py rate_movie 1 5 5```
  - Show in DataGrip: ```select * from rate```
    
- Users can watch a movie individually or they can play an entire collection.
  - Show in DataGrip: ```select * from watch_movie```
  - Watch a movie: ```python3 cli.py watch_movie 1 1```
  - Show in DataGrip: ```select * from watch_movie```
  - Watch a whole collection: ```python3 cli.py watch_collection 1 1```

- Users can follow another user. Users can search for new users to follow by email
- The application must also allow an user to unfollow a another user
  - Show in DataGrip: ```select * from following``` 
  - Follow: ```python3 cli.py follow_user 1 2```
  - Show in DataGrip: ```select * from following```
  - Unfollow: ```python3 cli.py unfollow_user 1```
  - Show in DataGrip: ```select * from following```
