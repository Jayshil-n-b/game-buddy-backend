import imp
import logging
from .modules.recommend.recommendOnGameId import recommendOnGameId
from .modules.recommend.recommendOnUsername import recommendOnUsername
from .modules.user.getFullUserInfo import getFullUserInfo
from .modules.game.getFullGameInfo import getFullGameInfo
from .modules.user.registerNewUserByJWT import registerNewUserByJWT
from .modules.user.loginUserByJWT import loginUserByJWT
from .modules.user.addHistory import addHistory
from .modules.user.toggleFavourite import toggleFavourite
from .modules.user.getFavourites import getFavourites
from .modules.recommend.recommendMix import recommendMix
from .modules.user.getCara import getCara
from .modules.recommend.recOnFavs import recOnFav
from .modules.user.getFavouritesListOfUser import getFavouritesListOfUser
from flask import Flask, jsonify, make_response, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

success_obj = {
    "msg": "Server is up and running...",
    "success": 200,
    "dataset_source": "https://www.kaggle.com/datasets/nikdavis/steam-store-games"
}


@app.route("/", methods=['GET'])
def basePage():
    return make_response(jsonify(success_obj), 200)


@app.route("/info/<int:appid>", methods=['GET'])
def getGameInfo(appid):
    return getFullGameInfo(appid)


@app.route('/recommend/<int:appid>', methods=['GET'])
def recommendGamesByGame(appid):
    return recommendOnGameId(appid)


@app.route('/getUser/<string:username>', methods=['GET'])
def getUserInfo(username):
    return getFullUserInfo(username)


@app.route('/getRecommendations', methods=['GET'])
@jwt_required()
def recommend():
    username = get_jwt_identity()
    return recommendMix(username)


@app.route("/userAverageRecommendations", methods=['GET'])
@jwt_required()
def recommendGamesByUsername():
    username = get_jwt_identity()
    return recommendOnUsername(username)


@app.route("/favouriteRecs", methods=['GET'])
@jwt_required()
def recommendOnFavourites():
    username = get_jwt_identity()
    return recOnFav(username)


@app.route('/register', methods=['POST'])
def registerUser():
    new_user = request.get_json()
    return registerNewUserByJWT(new_user)


@app.route('/login', methods=['POST'])
def loginUser():
    existing_user = request.get_json()
    return loginUserByJWT(existing_user)


@app.route('/addHistory', methods=['POST', 'GET'])
@jwt_required()
def protected():
    req = request.get_json()
    current_user = get_jwt_identity()
    return addHistory(req, current_user)


@app.route('/toggleFavourite', methods=['POST'])
@jwt_required()
def protected1():
    req = request.get_json()
    current_user = get_jwt_identity()
    return toggleFavourite(req['appid'], current_user)


@app.route('/getUsername', methods=['GET'])
@jwt_required()
def getUser():
    current_user = get_jwt_identity()
    return make_response({"username": current_user}, 200)


@app.route('/getFavourites', methods=['GET'])
@jwt_required()
def getFavouritesOfUser():
    current_user = get_jwt_identity()
    return getFavourites(current_user)


@app.route('/getFavouritesList', methods=['GET'])
@jwt_required()
def getFavouritesList():
    current_user = get_jwt_identity()
    return getFavouritesListOfUser(current_user)


@app.route('/carouselApps', methods=['GET'])
@jwt_required()
def getCarousel():
    current_user = get_jwt_identity()
    return getCara(current_user)


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods',
                         'GET,PUT,POST,DELETE,OPTIONS')
    return response
