# This python script creates an API by using 
# SQLite3 as its backend database

import flask
from flask import request, jsonify
#from flask_table import Table, Col

import sqlite3
from sqlite3 import Error

app = flask.Flask(__name__)
app.config['DEBUG'] = True


def dict_factory(cursor, row):
    '''This function returns the output of a query in the form of a dictionary'''
    
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def initialize_db():
    '''This function initializes the Database'''

    connect = sqlite3.connect('quotes.db')
    return connect

@app.route('/', methods=['GET'])
def home():
    '''This function shows the home page of the API'''
    return '''
    <h1>Welcome to the Awesome Quotes API</h1>
    '''

@app.route('/v1/quotes/all', methods=['GET'])
def all_data():
    '''This function fetches all the data present in the database'''
    connect = initialize_db()
    connect.row_factory = dict_factory
    cursor = connect.cursor()
    data = cursor.execute('''
    SELECT * FROM QUOTES;
    ''').fetchall()

    return jsonify(data)
                
@app.route('/v1/quotes', methods=['GET'])
def filterd_quote_data():
    '''This function fetches data based on the filter provided by the user'''
    query_parameters = request.args

    category = query_parameters.get('category')

    query = 'SELECT * FROM QUOTES WHERE'
    filters = []

    if category:
        query = query + ' category=? AND'
        filters.append(category)
    if not (category):
        page_not_found()
    
    # This removes everything till the fourth last character in the 
    # final query
    query = query[:-4] + ';'

    conn = initialize_db()
    conn.row_factory = dict_factory
    cursor = conn.cursor()

    data = cursor.execute(query, filters).fetchall()

    return jsonify(data)

# This function shows a error page if the API is not called correctly
@app.errorhandler(404)
def page_not_found():
    return '''
    <p>Ah oh, page not found :(</p>
    '''
if __name__ == "__main__":
    app.run()
    