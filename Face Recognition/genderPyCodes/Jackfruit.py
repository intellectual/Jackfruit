from pymongo import MongoClient
import datetime
import bottle, random
from pymongo import Connection
from bottle import route, debug, run, hook, request, response

 
DATABASE_HOST = 'localhost'
DATABASE_NAME = 'jackfruit'
DATABASE_PORT = 27017

client = MongoClient('localhost', 27017)
db = client.jackfruit
collection = db.analytics

json = {'timestamp' : 2312370, 'age_band' : 2, 'count' : 56, 'sex' : 'M', 'band1' : 2, 'band2' : 5, 'band3' : 6, 'gender1' : 4, 'gender2' : 6}

@hook('after_request')
def enable_cors():
    """
    You need to add some headers to each request.
    Don't use the wildcard '*' for Access-Control-Allow-Origin in production.
    """
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

@route('/')
def index():
    return "Please include timestamp in the URL"

@route('/timestamp/<time>', method=['OPTIONS', 'GET'])
def recipe_show( time=0 ):
	if request.method == 'OPTIONS':
		time = int(time)
		json = find(time)
		return json
	time = int(time)
	json = find(time)
	return json

def insert_into_mongo(json = json):
	insert_id = collection.insert(json)
	print "inserted into mongo"

def find(timestamp=0):
	if timestamp == 0:
		cursor = collection.find().sort("timestamp", -1)
		for doc in cursor:
			del doc['_id']
			return doc
	else:
		cursor = collection.find({"timestamp": {"$lte": timestamp}}).sort("timestamp", -1)
		for doc in cursor:
			del doc['_id']
			return doc


if __name__ == '__main__':
	cursor = find(0)
	print cursor
	debug(True)
	run(host='0.0.0.0', port=8000, reloader=True)




