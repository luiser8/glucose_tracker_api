from flask import Blueprint, jsonify, request
from middleware.verifyAuth import authorize
from services.hba1cSrv import hba1cSrv
from middleware.tokenJWTUtils import tokenJWTUtils

hba1c = Blueprint('hba1c', __name__)

class hba1cCtrl():

    @hba1c.route('/api/hba1c/get/start_date/<string:start_date>/end_date/<string:end_date>', methods=['GET'])
    @authorize
    def getByHba1c(start_date, end_date):
        user_id = tokenJWTUtils().getTokenUserId(request.headers)["user_id"]
        response = hba1cSrv().getByUserHba1cSrv(user_id, start_date, end_date)
        return jsonify(response), response["status"]

    @hba1c.route('/api/hba1c/post/calculate_dosis', methods=['POST'])
    @authorize
    def calculate_dosis():
        user_id = tokenJWTUtils().getTokenUserId(request.headers)["user_id"]
        data = request.get_json()
        payload = { "user_id": user_id, "actual_glucose": data.get("actual_glucose"), "objective_glucose": data.get("objective_glucose"), "carbohydrates": data.get("carbohydrates") }
        response = hba1cSrv().calculate_dosis(payload)
        return jsonify(response), response["status"]
