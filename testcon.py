import mysql.connector
from datetime import datetime

# Specify the format of the input string
# format_string = "%d/%m/%Y %H:%M"
# ja ta vindo formatado?

# Replace these values with your MySQL server information
host = 'database-1.cve8wekscbc9.us-east-2.rds.amazonaws.com'
user = 'admin'
password = 'renan123'
database = 'db_projn'  # Replace with your actual database name

# Establish a connection to the MySQL server
connection = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=database
)

# Create a cursor object to interact with the database
cursor = connection.cursor()

print('connected!')