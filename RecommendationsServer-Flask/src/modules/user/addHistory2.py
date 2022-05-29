import json
from urllib import response
from flask import jsonify, make_response
from pymongo import MongoClient
import os
from bson import json_util

client = MongoClient(os.getenv("CONNSTR"))

db = client["gameBuddyDb"]
userCollection = db.usersData


def addHistory2(req, currUser):
    # userCollection.update_one(
    #     {"username": currUser},
    #     {"$push": {"history": req}}
    # )
    # response = make_response(jsonify({"req": req, "user": currUser}), 200)
    # response.headers.add('Access-Control-Allow-Origin', '*')
    # return response
    gameHistory = userCollection.find_one(
        {"$and": [{"username": currUser}, {"history.appid": req['appid']}]})
    if gameHistory:
        time = 0
        list = gameHistory['history']
        for h in list:
            if h['appid'] == req['appid']:
                time = h['time']
                break
        userCollection.update_one(
            {"$and": [{"username": currUser}, {"history.appid": req['appid']}]}, {"$pull": {"history": {"appid": req['appid']}}})
        userCollection.update_one(
            {"username": currUser}, {"$push": {"history": {"appid": req['appid'], "time": time + req['time']}}})
        response = make_response(
            jsonify(json.loads(json_util.dumps(gameHistory))))
    else:
        userCollection.update_one(
            {"username": currUser}, {"$push": {"history": {"appid": req['appid'], "time": req['time']}}})
        response = make_response(jsonify({"msg": "Nahi Hai!!"}))
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
