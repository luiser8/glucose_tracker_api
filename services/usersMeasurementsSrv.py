from flask import flash
from repository.repoSQL import repoSQL
from middleware.responseHttpUtils import responseHttpUtils

class usersMeasurementsSrv():
    def __init__(self):
        self.query_service = repoSQL('users_measurements', ['id', 'user_id', 'date', 'hour', 'value'])

    def getAllByUserIdSrv(self, user_id):
        response = self.query_service.get_by_conditions({
            "user_id": user_id
        })
        #response =  self.query_service.get_all()
        if response:
            return responseHttpUtils().response("Measurements founds successfully", 200, response)
        else:
            return responseHttpUtils().response("Error listing measurements", 400, response)

    def getByIdSrv(self, id):
        response = self.query_service.get_by_id(id)
        if response:
            return responseHttpUtils().response("Measurements found by id successfully", 200, response)
        else:
            return responseHttpUtils().response("Error listing measurements not found", 404, response)

    def postSrv(self, payload):
        if payload:
            meas_data = {
                'user_id': payload["user_id"],
                "date": payload["date"],
                "hour": payload["hour"],
                "value": payload["value"]
            }
            if "user_id" in payload:
                meas_data["user_id"] = payload["user_id"]

            result = self.query_service.insert(meas_data)
            if result:
                return responseHttpUtils().response("Measurements add successfully", 201, result)
            else:
                return responseHttpUtils().response("Error add measurements", 400, result)

    def putSrv(self, id, payload):
        if payload:
            meas_data = {
                'user_id': payload["user_id"],
                "date": payload["date"],
                "hour": payload["hour"],
                "value": payload["value"]
            }
            if "id" in payload:
                meas_data["id"] = payload["id"]

            result = self.query_service.update(id, meas_data)
            if result:
                return responseHttpUtils().response("Measurements update successfully", 200, result)
            else:
                return responseHttpUtils().response("Error update measurements", 400, result)

    def deleteSrv(self, id):
        if id:
            result = self.query_service.delete(id)
            if result:
                return responseHttpUtils().response("Measurements deleting successfully", 200, result)
            else:
                return responseHttpUtils().response("Error deleting measurements", 400, result)