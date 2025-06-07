from repository.repoSQL import repoSQL
from middleware.responseHttpUtils import responseHttpUtils

class usersRegistrationSrv():
    def __init__(self):
        self.result = None
        self.query_service = repoSQL('users_registration', ['id', 'user_id', 'type', 'code', 'status', 'createdat'])

    def getByIdSrv(self, id, type):
        response = self.query_service.get_by_conditions({
            "user_id": id,
            "type": type
        })
        return responseHttpUtils().response(None, None, response)

    def getByCodeSrv(self, type, code):
        response = self.query_service.get_by_conditions({
            "code": code,
            "type": type
        })
        return responseHttpUtils().response(None, None, response)

    def getByCodeAndUserIdSrv(self, type, code, user_id):
        response = self.query_service.get_by_conditions({
            "user_id": user_id,
            "code": code,
            "type": type
        })
        return responseHttpUtils().response(None, None, response)

    def postSrv(self, payload):
        if not payload:
            return responseHttpUtils().response("Payload is required", None, None)

        user_data = {
            "user_id": payload["user_id"],
            "type": payload["type"],
            "code": payload["code"],
            "status": payload["status"]
        }

        user_registration_exists = self.getByIdSrv(payload["user_id"], payload["type"])

        if user_registration_exists and user_registration_exists[0]["status"]:
            return responseHttpUtils().response("User ID match stored user", None, None)
        else:
            self.result = self.query_service.insert(user_data)

        return self.result

    def putSrv(self, id, payload):
        if not payload:
            return responseHttpUtils().response("Payload is required", None, None)

        user_data = {
            "user_id": payload["user_id"],
            "type": payload["type"],
            "code": payload["code"],
            "status": payload["status"]
        }
        if id:
            user_data["user_id"] = payload["user_id"]
        if "status" in payload:
            user_data["status"] = payload["status"]

        self.result = self.query_service.update(id, user_data)

        if self.result:
            return responseHttpUtils().response(None, None, self.result)
        return responseHttpUtils().response("User error updating", None, None)

    def deleteSrv(self, id, type):
        if id:
            user = self.getByIdSrv(id, type)
            response = self.query_service.delete(user[0]["id"])
            return responseHttpUtils().response(None, None, response)