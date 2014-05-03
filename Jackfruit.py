import bottle, random
from bottle import route, jinja2_view as view, debug, run
 
DATABASE_HOST = 'localhost'
DATABASE_NAME = 'jackfruit'
DATABASE_PORT = 27017

import pymongo
from pymongo import Connection
connection = Connection(DATABASE_HOST, DATABASE_PORT)
db = connection[DATABASE_NAME]
users = db.analytics

@route('/')
def index():
    return "Please include timestamp in the URL"



if __name__ == '__main__':
    debug(True)
    run(host='localhost', port=8000, reloader=True)

