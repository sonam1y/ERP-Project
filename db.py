import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="sonam",
        password="sonam9355",
        database="erp_system"
    )