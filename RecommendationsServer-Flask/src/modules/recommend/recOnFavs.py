from flask import jsonify, make_response
import pickle
from pathlib import Path
import pandas as pd
from pymongo import MongoClient
import os
from iteration_utilities import unique_everseen
import random
import numpy as np
from numpy.linalg import norm

HERE = Path(__file__).parent

# similarity = pickle.load(open(HERE / '../../static/similarity_dump.pkl', 'rb'))
processed_df = pd.DataFrame(pickle.load(
    open(HERE / '../../static/processed_df_dump.pkl', 'rb')))
vectors = pickle.load(open(HERE / '../../static/vectors_dump.pkl', 'rb'))

client = MongoClient(os.getenv("CONNSTR"))

db = client["gameBuddyDb"]
userCollection = db.usersData
gameCollection = db.gamesData


def recommendOnAppid(appid, n):
    recommendations = []

    game_index = processed_df[processed_df['appid'] == appid]

    if game_index.shape[0] == 0:
        return make_response(
            jsonify({'success': False, 'msg': f"Game with name {appid} not found"}), 404)

    game_index = game_index.index[0]
    myVector = np.array(processed_df[processed_df['appid']
                                     == appid].iloc[0]['myNewTags'])
    # distances = similarity[game_index]
    distances = np.dot(vectors, myVector) / \
        (norm(vectors, axis=1)*norm(vectors))
    game_list = sorted(list(enumerate(distances)),
                       reverse=True, key=lambda x: x[1])[1:n+1]

    for game in game_list:
        rec = {}
        rec['name'] = processed_df.iloc[game[0]]['name']
        rec['appid'] = int(processed_df.iloc[game[0]]['appid'])
        rec['header_image'] = processed_df.iloc[game[0]]['header_image']
        recommendations.append(rec)

    return recommendations


def recOnFav(username):
    recommendations = []
    userData = userCollection.find_one({"username": username})
    length = len(userData['favourites'])
    print(userData)

    for i in userData['favourites']:
        currPer = int(100/length)
        currRec = recommendOnAppid(i, currPer)
        for rec in currRec:
            recommendations.append(rec)
        # recommendations.append(i)
    # recommendations.append(userData)

    recommendations = list(unique_everseen(recommendations))
    random.shuffle(recommendations)

    return make_response(jsonify({"recommendations": recommendations, "success": True}), 200)
