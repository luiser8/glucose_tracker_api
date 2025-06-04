from flask import Blueprint, request, jsonify
from middleware.rateLimit import rate_limit
from middleware.tokenJWTUtils import tokenJWTUtils
from middleware.verifyAuth import authorize
from services.authSrv import authSrv
from schemas.AuthSchema import AuthSchema

auth = Blueprint('auth', __name__)

class authCtrl():

    @auth.route('/api/auth/login', methods=['POST'])
    @rate_limit()
    def login():
        payload = AuthSchema().load(request.get_json())
        response = authSrv().loginSrv(payload)
        return jsonify(response), response["status"]

    @auth.route('/api/auth/logout', methods=['POST'])
    @authorize
    @rate_limit()
    def logout():
        response = None
        user_id = tokenJWTUtils().getTokenUserId(request.headers)["user_id"]
        response = authSrv().destroySrv(user_id)
        return jsonify(response), response["status"]

    @auth.route('/api/auth/refresh', methods=['POST'])
    @authorize
    @rate_limit()
    def refresh():
        response = None
        user_id = tokenJWTUtils().getTokenUserId(request.headers)["user_id"]
        response = authSrv().refreshSrv(user_id)
        return jsonify(response), response["status"]