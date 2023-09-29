import mysql.connector
from mysql.connector import Error

# Stores users and their corresponding data
class UserStorage:
    """
        database_path: points to file treated as sql database
    """
    def __init__(self):
        self.connection = self.create_server_connection("localhost", "root", "")
        self.execute("SET autocommit = 1;")
        self.execute("CREATE DATABASE leetcode_enforcer;")
        self.execute("USE leetcode_enforcer;")
        self.execute("CREATE TABLE users (discord_username varchar(50), leetcode_username varchar(50));")

    def register_user(self, discord_username, leetcode_username):
        self.execute(f"INSERT INTO users VALUES (\"{discord_username}\", \"{leetcode_username}\");")

    def get_leetcode_username_from_discord(self, discord_username):
        return self.fetchone(f"SELECT DISTINCT leetcode_username FROM users WHERE discord_username=\"{discord_username}\";")

    def create_server_connection(self, host_name, user_name, user_password):
        connection = None
        try:
            connection = mysql.connector.connect(
                host=host_name,
                user=user_name,
                passwd=user_password
            )
            print("MySQL Database connection successful")
        except Error as err:
            print(f"Error: '{err}'")

        return connection
    
    def fetchone(self, query):
        cursor = self.connection.cursor(buffered=True)
        try:
            cursor.execute(query)
            result = cursor.fetchone()
            print(f"Query executed successfully: {query}")
            if result:
                return result[0]
        except Error as err:
            print(f"Error: '{err}'")

    def execute(self, query):
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            print(f"Query executed successfully: {query}")
        except Error as err:
            print(f"Error: '{err}'")
