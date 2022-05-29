import hashlib
from flask import make_response, jsonify
from pymongo import MongoClient
import os
from flask_jwt_extended import create_access_token

client = MongoClient(os.getenv("CONNSTR"))

db = client["gameBuddyDb"]
userCollection = db.usersData


def loginUserByJWT(existing_user):
    user_from_db = userCollection.find_one(
        {'username': existing_user['username']})

    if user_from_db:
        encrpted_password = hashlib.sha256(
            existing_user['password'].encode("utf-8")).hexdigest()

        if encrpted_password == user_from_db['password']:
            access_token = create_access_token(
                identity=user_from_db['username'])  # create jwt token
            return make_response(jsonify(access_token=access_token), 200)
        else:
            return make_response(jsonify({'msg': "Invalid Password"}), 401)
    else:
        return make_response(jsonify({'msg': 'Invalid Username'}), 401)
