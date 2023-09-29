import mysql.connector
from mysql.connector import Error
from typing import List

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

        self.execute("DROP TABLE users;")
        self.execute("DROP TABLE user_roles;") 
        self.execute("DROP TABLE metadata;")

        self.execute("CREATE TABLE users (discord_id BIGINT, leetcode_username VARCHAR(50));")
        self.execute("CREATE TABLE user_roles (discord_id BIGINT, role_id BIGINT);")
        self.execute("CREATE TABLE metadata (leetcode_role_id BIGINT);")

    def register_user(self, discord_id, leetcode_username, role_ids):
        self.execute(f"INSERT INTO users VALUES ({discord_id}, \"{leetcode_username}\");")
        for rid in role_ids:
            self.execute(f"INSERT INTO user_roles VALUES({discord_id}, {rid});")

    def get_leetcode_username_from_discord(self, discord_id):
        return self.fetchone(f"SELECT DISTINCT leetcode_username FROM users WHERE discord_id=\"{discord_id}\";")

    def get_user_roles(self, discord_id: int):
        data = self.fetchall(f'SELECT DISTINCT role_id FROM user_roles WHERE discord_id="{discord_id}";')
        if data == None:
            return []
        rids = list(map(lambda data: data[0], data))
        return rids

    def register_leetcode_role(self, leetcode_role_id: int): 
        self.execute(f"INSERT INTO metadata VALUES ({leetcode_role_id});")

    def unregister_leetcode_role(self):
        self.execute("TRUNCATE TABLE metadata;")

    def get_leetcode_rid(self):
        return self.fetchone(f"SELECT DISTINCT leetcode_role_id FROM metadata;")

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
    
    def fetchall(self, query):
        cursor = self.connection.cursor(buffered=True)
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            print(f"Query executed successfully: {query}")
            if result:
                return result
        except Error as err:
            print(f"Error: '{err}'")

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
