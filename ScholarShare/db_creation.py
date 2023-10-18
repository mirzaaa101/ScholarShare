# intall mysql workbench on your local machine
# pip install mysql
# pip install mysql-connector
# pip install mysql-connector-python

import mysql.connector

mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    passwd='rootroot'
)

# Create cursor object
cursorObj = mydb.cursor()

# Create database
cursorObj.execute("CREATE DATABASE IF NOT EXISTS scholarshare")

# Connect to the 'crm' database
cursorObj.execute("USE scholarshare")

print("Database has been created!!")