from flask import Flask, jsonify, abort, request, url_for
from flask_bootstrap import Bootstrap
from flask.ext.pymongo import PyMongo


from bson.objectid import ObjectId
from .session import MongoSessionInterface


app = Flask(__name__)
Bootstrap(app)
mongo = PyMongo(app)

app.secret_key = 'thisissupersecret'
app.session_interface = MongoSessionInterface(db='pjuu')

from activitylog import views