import json
from flask import jsonify, make_response
from pymongo import MongoClient
import os
from bson import json_util

client = MongoClient(os.getenv("CONNSTR"))

db = client["gameBuddyDb"]
userCollection = db.usersData


def getFavourites(currUser):
    userData = userCollection.find_one({"username": currUser})
    response = make_response(jsonify(userData["favourites"]), 200)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
    # return make_response({"hii": "hii"}, 200)
