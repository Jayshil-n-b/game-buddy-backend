import json
from flask import jsonify, make_response
from pymongo import MongoClient
import os
from bson import json_util
import pymongo

client = MongoClient(os.getenv("CONNSTR"))

db = client["gameBuddyDb"]
userCollection = db.usersData
gameCollection = db.gamesData


def getCara(currUser):
    userData = userCollection.find_one({"username": currUser})
    L = []
    for genres in userData['genres']:
        R = gameCollection.find({"steamspy_tags": genres}).sort(
            "owners", pymongo.DESCENDING).limit(1)
        L.append(json.loads(json_util.dumps(R)))

    response = make_response(jsonify(L), 200)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
    # return make_response({"hii": "hii"}, 200)
