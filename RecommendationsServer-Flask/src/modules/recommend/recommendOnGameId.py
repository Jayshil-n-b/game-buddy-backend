from flask import jsonify, make_response
import pickle
from pathlib import Path
import pandas as pd
import numpy as np
from numpy.linalg import norm

HERE = Path(__file__).parent

# similarity = pickle.load(open(HERE / '../../static/similarity_dump.pkl', 'rb'))
processed_df = pd.DataFrame(pickle.load(
    open(HERE / '../../static/processed_df_dump.pkl', 'rb')))
vectors = pickle.load(open(HERE / '../../static/vectors_dump.pkl', 'rb'))


def recommendOnGameId(appid):
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
                       reverse=True, key=lambda x: x[1])[1:21]

    for game in game_list:
        rec = {}
        rec['name'] = processed_df.iloc[game[0]]['name']
        rec['appid'] = int(processed_df.iloc[game[0]]['appid'])
        rec['header_image'] = processed_df.iloc[game[0]]['header_image']
        recommendations.append(rec)

    return make_response(jsonify({"recommendations": recommendations, "success": True}), 200)
