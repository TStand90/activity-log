from flask import Flask, jsonify, abort, request, url_for
from flask_bootstrap import Bootstrap
from flask.ext.pymongo import PyMongo


# from pymongo import MongoClient
from bson.objectid import ObjectId


app = Flask(__name__)
Bootstrap(app)
mongo = PyMongo(app)

# client = MongoClient()
# db = client.flask_activity_log
# collection = db.activities

app.secret_key = 'thisissupersecret'

from app import views