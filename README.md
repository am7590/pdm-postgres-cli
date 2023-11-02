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
