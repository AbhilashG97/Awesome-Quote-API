import json
import sqlite3
from sqlite3 import Error

def create_connection():
    try:
        connection = sqlite3.connect('quotes.db')
        return connection
    except Error:
        print(Error)

def create_quotes_table(connection):
    '''This function creates a QUOTES Table'''
    cursor_obj = connection.cursor()
    cursor_obj.execute('''
        CREATE TABLE QUOTES(
            id text,
            quote text,
            author text,
            category text
        )
    ''')
    connection.commit()

def insert_values(connection):
    '''This function inserts values into all the quotes table by reading the data from a json data file'''
    cursor_object = connection.cursor()

    with open('quotes.json') as data_file:    
        data = json.load(data_file)
        index = 0
        for quote in data:
            quote_name = quote['Quote']
            author_name = quote['Author']
            category_name = quote['Category']
            # print('INSERT INTO QUOTES values (' + str(index) + ',' + quote_name + ',' + author_name + ',' + category_name + ')')
            cursor_object.execute('''INSERT INTO QUOTES values (?, ?, ?, ?)''', (str(index), quote_name, author_name, category_name))
            index += 1
            connection.commit()

connection = create_connection()

try:
    create_quotes_table(connection)
except: 
    print('Oops, Database is already created!')

try:
    insert_values(connection)
except:
    print('Error inserting values :(')