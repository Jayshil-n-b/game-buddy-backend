from flask import jsonify, make_response
import json
from bson import json_util
from pymongo import MongoClient
import os

client = MongoClient(os.getenv("CONNSTR"))

db = client["gameBuddyDb"]
collection = db.gamesData


def getFullGameInfo(appid):
    bsonObject = (collection.find_one({'appid': appid}))
    if bsonObject:
        jsonObject = json.loads(json_util.dumps(bsonObject))
        jsonObject['success'] = True
        return make_response(jsonify(jsonObject), 200)
    else:
        jsonObject = {
            "msg": f"Game with id {appid} does not exits.", 'success': False}
        return make_response(jsonify(jsonObject), 404)
