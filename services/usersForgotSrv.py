from repository.repoSQL import repoSQL
from middleware.responseHttpUtils import responseHttpUtils

class usersForgotSrv():
    def __init__(self):
        self.result = None
        self.query_service = repoSQL('users_forgot_password', ['id', 'user_id', 'code', 'createdat', 'status'])

    def getByIdSrv(self, id):
        response = self.query_service.get_by_conditions({
            "user_id": id
        })
        return responseHttpUtils().response(None, None, response)

    def getByCodeSrv(self, code):
        response = self.query_service.get_by_conditions({
            "code": code
        })
        return responseHttpUtils().response(None, None, response)

    def postSrv(self, payload):
        if not payload:
            return responseHttpUtils().response("Payload is required", None, None)

        user_data = {
            "user_id": payload["user_id"],
            "code": payload["code"]
        }

        user_forgot_exists = self.getByIdSrv(payload["user_id"])

        if user_forgot_exists and user_forgot_exists[0]["status"]:
            return responseHttpUtils().response("User ID match stored user", None, None)
        else:
            self.result = self.query_service.insert(user_data)

        return self.result

    def putSrv(self, id, payload):
        if not payload:
            return responseHttpUtils().response("Payload is required", None, None)
        user_data = {
            "user_id": payload["user_id"],
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

    def deleteSrv(self, id):
        if id:
            user = self.getByIdSrv(id)
            response = self.query_service.delete(user[0]["id"])
            return responseHttpUtils().response(None, None, response)