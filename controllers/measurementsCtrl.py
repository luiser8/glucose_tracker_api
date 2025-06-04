from flask import Blueprint, request, jsonify
from middleware.rateLimit import rate_limit
from middleware.verifyAuth import authorize
from services.usersMeasurementsSrv import usersMeasurementsSrv
from middleware.tokenJWTUtils import tokenJWTUtils
from schemas.measurementsSchema import MeasurementsSchema

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

    @measurements.route('/api/measurements/get/start_date/<string:start_date>/end_date/<string:end_date>', methods=['GET'])
    @authorize
    def getByDateRange(start_date, end_date):
        user_id = tokenJWTUtils().getTokenUserId(request.headers)["user_id"]
        response = usersMeasurementsSrv().getByDateRangeSrv(user_id, start_date, end_date)
        return jsonify(response), response["status"]

    @measurements.route('/api/measurements/post', methods=['POST'])
    @authorize
    @rate_limit()
    def post():
        user_id = tokenJWTUtils().getTokenUserId(request.headers)["user_id"]
        payload = MeasurementsSchema().load(request.get_json())
        response = usersMeasurementsSrv().postSrv(user_id, payload)
        return jsonify(response), response["status"]

    @measurements.route('/api/measurements/put/<int:id>', methods=['PUT'])
    @authorize
    @rate_limit()
    def put(id):
        user_id = tokenJWTUtils().getTokenUserId(request.headers)["user_id"]
        payload = MeasurementsSchema().load(request.get_json())
        response = usersMeasurementsSrv().putSrv(id, user_id, payload)
        return jsonify(response), response["status"]

    @measurements.route('/api/measurements/delete/<int:id>', methods=['DELETE'])
    @authorize
    @rate_limit()
    def delete(id):
        request = usersMeasurementsSrv().deleteSrv(id)
        return jsonify(request), request["status"]