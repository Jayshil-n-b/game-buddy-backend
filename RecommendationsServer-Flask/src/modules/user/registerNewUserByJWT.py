import hashlib
from flask import make_response, jsonify
from pymongo import MongoClient
import os

client = MongoClient(os.getenv("CONNSTR"))

db = client["gameBuddyDb"]
userCollection = db.usersData


def registerNewUserByJWT(new_user):
    new_user["password"] = hashlib.sha256(
        new_user["password"].encode("utf-8")).hexdigest()

    user = userCollection.find_one({"username": new_user["username"]})
    if user:
        return make_response(jsonify({'msg': 'Username already exists'}), 409)
    else:
        userCollection.insert_one(new_user)
        return make_response(jsonify({'msg': 'User created successfully'}), 201)
