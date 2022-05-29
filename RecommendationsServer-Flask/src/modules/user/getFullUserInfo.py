from flask import make_response, jsonify
import json
from bson import json_util
from pymongo import MongoClient
import os

client = MongoClient(os.getenv("CONNSTR"))

db = client["gameBuddyDb"]
userCollection = db.usersData


def getFullUserInfo(a):
    bsonObject = (userCollection.find_one({'username': a}))
    if bsonObject:
        jsonObject = json.loads(json_util.dumps(bsonObject))
        jsonObject['success'] = True
        return make_response(jsonify(jsonObject), 200)
    else:
        jsonObject = {
            "msg": f"User with username {a} does not exits.", 'success': False}
        return make_response(jsonify(jsonObject), 404)
