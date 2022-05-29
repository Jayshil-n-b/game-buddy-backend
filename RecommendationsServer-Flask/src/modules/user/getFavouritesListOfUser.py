import json
from flask import jsonify, make_response
from pymongo import MongoClient
import os
from bson import json_util

client = MongoClient(os.getenv("CONNSTR"))

db = client["gameBuddyDb"]
userCollection = db.usersData
gameCollection = db.gamesData


def getFavouritesListOfUser(currUser):
    L = []
    userData = userCollection.find_one({"username": currUser})
    list = userData["favourites"]
    for i in list:
        game = gameCollection.find_one({"appid": i})
        R = {}
        R['appid'] = game['appid']
        R['header_image'] = game['header_image']
        R['name'] = game['name']
        L.append(R)
    response = make_response(
        jsonify({"recommendations": L, "success": True}), 200)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
    # return make_response({"hii": "hii"}, 200)
