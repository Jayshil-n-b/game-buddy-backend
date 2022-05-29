import json
from flask import jsonify, make_response
from pymongo import MongoClient
import os
from bson import json_util

client = MongoClient(os.getenv("CONNSTR"))

db = client["gameBuddyDb"]
userCollection = db.usersData


def toggleFavourite(appid, currUser):
    userData = userCollection.find_one({"username": currUser})
    if appid in userData['favourites']:
        userCollection.update_one({"username": currUser}, {
            "$pull": {"favourites": appid}})
        response = make_response(jsonify({"msg": "Removed!!"}))
    else:
        userCollection.update_one({"username": currUser}, {
            "$push": {"favourites": appid}})
        response = make_response(jsonify({"msg": "Added!!"}))
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
