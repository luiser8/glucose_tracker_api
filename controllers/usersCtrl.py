from flask import Blueprint, request, jsonify
from middleware.rateLimit import rate_limit
from services.usersSrv import usersSrv
from middleware.verifyAuth import authorize
from schemas.userSchema import UserSchema, ChangePasswordSchema
from schemas.confirmationRegisterSchema import ConfirmRegistrationSchema

users = Blueprint('users', __name__)

class usersCtrl():
    @users.route('/api/users/get', methods=['GET'])
    @authorize
    @rate_limit()
    def getAll():
        response = usersSrv().getAllSrv()
        return jsonify(response), response["status"]

    @users.route('/api/users/get/<int:id>', methods=['GET'])
    @authorize
    @rate_limit()
    def getById(id):
        response = usersSrv().getByIdSrv(id)
        return jsonify(response), response["status"]

    @users.route('/api/users/post', methods=['POST'])
    @rate_limit()
    def post():
        payload = UserSchema().load(request.get_json())
        response = usersSrv().postSrv(payload)
        return jsonify(response), response["status"]

    @users.route('/api/users/put/<int:id>', methods=['PUT'])
    @authorize
    @rate_limit()
    def put(id):
        payload = UserSchema().load(request.get_json())
        response = usersSrv().putSrv(id, payload)
        return jsonify(response), response["status"]

    @users.route('/api/users/delete/<int:id>', methods=['DELETE'])
    @authorize
    @rate_limit()
    def delete(id):
        response = usersSrv().deleteSrv(id)
        return jsonify(response), response["status"]

    @users.route('/api/users/forgot_password/<string:email>', methods=['GET'])
    def forgotPassword(email):
        result = usersSrv().forgotPasswordSrv(email)
        return jsonify(result), result["status"]

    @users.route('/api/users/change_password', methods=['POST'])
    def changePassword():
        payload = ChangePasswordSchema().load(request.get_json())
        result = usersSrv().changePasswordSrv(payload)
        return jsonify(result), result["status"]

    @users.route('/api/users/confirm_registration', methods=['POST'])
    def confirmRegistration():
        payload = ConfirmRegistrationSchema().load(request.get_json())
        result = usersSrv().confirmRegistrationSrv(payload)
        return jsonify(result), result["status"]