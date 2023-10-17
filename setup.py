# Get database credentials from the database_credentials.py
def get_database_credentials():
    with open("database_credentials.txt") as file:
        lines = file.readlines()
        credentials = {}
        for line in lines:
            key, value = line.strip().split('=')
            credentials[key] = value
    return credentials

db_credentials = get_database_credentials()

# SSH tunnel configuration
ssh_config = {
    "ssh_address_or_host": "starbug.cs.rit.edu",
    "ssh_username": db_credentials["DB_USER"],
    "ssh_password": db_credentials["DB_PASSWORD"],
    "ssh_port": 22,
}

# PostgreSQL connection parameters
db_params = {
    "host": "127.0.0.1",
    "port": 5432,
    "database": "p320_12",
    "user": db_credentials["DB_USER"],
    "password": db_credentials["DB_PASSWORD"],
}