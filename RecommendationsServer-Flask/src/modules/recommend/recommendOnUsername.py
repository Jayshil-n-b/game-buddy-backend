from flask import make_response, jsonify
import numpy as np
import pandas as pd
from numpy.linalg import norm
from pymongo import MongoClient
import os
import pickle
from pathlib import Path

client = MongoClient(os.getenv("CONNSTR"))

db = client["gameBuddyDb"]
userCollection = db.usersData

HERE = Path(__file__).parent
processed_df = pd.DataFrame(pickle.load(
    open(HERE / '../../static/processed_df_dump.pkl', 'rb')))
vectors = pickle.load(open(HERE / '../../static/vectors_dump.pkl', 'rb'))


def getMyVector(bsonObject):
    totalPlayTime = 0
    L = np.zeros(371)
    # print(bsonObject['history'])
    for h in bsonObject['history']:
        totalPlayTime += h['time']
        currGameId = h['appid']
        L = L + (h['time'])*np.array(processed_df[processed_df['appid']
                                                  == currGameId].iloc[0]['myNewTags'])
    # print(totalPlayTime)
    return L/totalPlayTime


def recommendOnUsername(username):
    bsonObject = (userCollection.find_one({'username': username}))
    if bsonObject:
        myVector = getMyVector(bsonObject)
        distances = np.dot(vectors, myVector) / \
            (norm(vectors, axis=1)*norm(vectors))
        game_list = sorted(list(enumerate(distances)),
                           reverse=True, key=lambda x: x[1])[1:51]
        F = []
        for i in game_list:
            R = {}
            R['name'] = (processed_df.iloc[i[0]]['name'])
            R['appid'] = int(processed_df.iloc[i[0]]['appid'])
            R['header_image'] = processed_df.iloc[i[0]]['header_image']
            F.append(R)
        response = make_response(
            jsonify({"recommendations": F, "success": True}), 200)
    else:
        jsonObject = {
            "msg": f"User with username {username} does not exits.", 'success': False}
        response = make_response(jsonify(jsonObject), 404)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
