from flask import Blueprint, request, jsonify
from middleware.verifyAuth import authorize
from services.usersMeasurementsSrv import usersMeasurementsSrv
from middleware.tokenJWTUtils import tokenJWTUtils

measurements = Blueprint('measurements', __name__)

class publicationsCtrl():
    @measurements.route('/api/measurements/get', methods=['GET'])
    @authorize
    def getAllByUser():
        user_id = tokenJWTUtils().getTokenUserId(request.headers)["user_id"]
        response = usersMeasurementsSrv().getAllByUserIdSrv(user_id)
        return jsonify(response), response["status"]

    @measurements.route('/api/measurements/get/<int:id>', methods=['GET'])
    @authorize
    def getById(id):
        response = usersMeasurementsSrv().getByIdSrv(id)
        return jsonify(response), response["status"]

    @measurements.route('/api/measurements/post', methods=['POST'])
    @authorize
    def post():
        user_id = tokenJWTUtils().getTokenUserId(request.headers)["user_id"]
        data = request.get_json()
        payload = { "user_id": user_id, "date": data.get("date"), "hour": data.get("hour"), "value": data.get("value") }
        save = usersMeasurementsSrv().postSrv(payload)
        return jsonify(save), save["status"]

    @measurements.route('/api/measurements/put/<int:id>', methods=['PUT'])
    @authorize
    def put(id):
        user_id = tokenJWTUtils().getTokenUserId(request.headers)["user_id"]
        data = request.get_json()
        payload = { "user_id": user_id, "date": data.get("date"), "hour": data.get("hour"), "value": data.get("value") }
        save = usersMeasurementsSrv().putSrv(id, payload)
        return jsonify(save), save["status"]

    @measurements.route('/api/measurements/delete/<int:id>', methods=['DELETE'])
    @authorize
    def delete(id):
        save = usersMeasurementsSrv().deleteSrv(id)
        return jsonify(save), save["status"]