from flask import Blueprint, request, jsonify
from services.usersSrv import usersSrv
from middleware.verifyAuth import authorize

users = Blueprint('users', __name__)

class usersCtrl():
    @users.route('/api/users/get', methods=['GET'])
    @authorize
    def getAll():
        response = usersSrv().getAllSrv()
        return jsonify(response), response["status"]

    @users.route('/api/users/get/<int:id>', methods=['GET'])
    @authorize
    def getById(id):
        response = usersSrv().getByIdSrv(id)
        return jsonify(response), response["status"]

    @users.route('/api/users/post', methods=['POST'])
    def post():
        data = request.get_json()
        payload = { "firstname": data.get("firstname"), "lastname": data.get("lastname"), "email": data.get("email"), "password": data.get("password") }
        save = usersSrv().postSrv(payload)
        return jsonify(save), save["status"]

    @users.route('/api/users/put/<int:id>', methods=['PUT'])
    @authorize
    def put(id):
        data = request.get_json()
        payload = { "firstname": data.get("firstname"), "lastname": data.get("lastname"), "email": data.get("email"), "password": data.get("password"), "status": data.get("status") }
        save = usersSrv().putSrv(id, payload)
        return jsonify(save), save["status"]

    @users.route('/api/users/delete/<int:id>', methods=['DELETE'])
    @authorize
    def delete(id):
        save = usersSrv().deleteSrv(id)
        return jsonify(save), save["status"]

    @users.route('/api/users/forgot_password/<string:email>', methods=['GET'])
    def forgotPassword(email):
        result = usersSrv().forgotPasswordSrv(email)
        return jsonify(result), result["status"]

    @users.route('/api/users/change_password', methods=['POST'])
    def changePassword():
        data = request.get_json()
        payload = { "code": data.get("code"), "email": data.get("email"), "newpassword": data.get("newpassword") }
        result = usersSrv().changePasswordSrv(payload)
        return jsonify(result), result["status"]