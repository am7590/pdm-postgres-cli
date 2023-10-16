import psycopg2
import paramiko
from sshtunnel import SSHTunnelForwarder  # Install sshtunnel using pip if not already installed

# Get database credentials from the file
# Function to read database credentials from the file
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
    cursor.execute("SELECT version()")
    version = cursor.fetchone()
    print("PostgreSQL version:", version)

    cursor.close()
    conn.close()
