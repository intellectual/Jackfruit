from pymongo import MongoClient
import datetime
import bottle, random
from pymongo import Connection
from bottle import route, debug, run

 
DATABASE_HOST = 'localhost'
DATABASE_NAME = 'jackfruit'
DATABASE_PORT = 27017

client = MongoClient('localhost', 27017)
db = client.jackfruit
collection = db.analytics

json = {'timestamp' : 2312370, 'age_band' : 2, 'count' : 56, 'sex' : 'M', 'band1' : 2, 'band2' : 5, 'band3' : 6, 'gender1' : 4, 'gender2' : 6}

@route('/')
def index():
    return "Please include timestamp in the URL"

@route('/timestamp/<time>', method='GET')
def recipe_show( time=0 ):
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




