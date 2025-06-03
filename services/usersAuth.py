from datetime import datetime
from repository.repoSQL import repoSQL
from middleware.responseHttpUtils import responseHttpUtils

class usersAuthSrv():
    def __init__(self):
        self.result = None
        self.query_service = repoSQL('users_auth', ['id', 'user_id', 'access_token', 'refresh_token', 'createdat', 'updatedat'])

    def getByIdSrv(self, id):
        response = self.query_service.get_by_conditions({
            "user_id": id
        })
        return responseHttpUtils().response(None, None, response)

    def postSrv(self, payload):
        if not payload:
            return responseHttpUtils().response("Payload is required", None, None)

        user_data = {
            "user_id": payload["user_id"],
            "access_token": payload["access_token"],
            "refresh_token": payload["refresh_token"],
            "createdat": datetime.now()
        }

        user_exists = self.getByIdSrv(payload["user_id"])

        if user_exists:
            if payload["user_id"] == user_exists[0]["user_id"]:
                user_data["updatedat"] = datetime.now()
                self.result =self.query_service.update(user_exists[0]["id"], user_data)
            else:
                return responseHttpUtils().response("User ID does not match stored user", None, None)
        else:
            self.result =self.query_service.insert(user_data)

        return responseHttpUtils().response(None, None, self.result)

    def deleteSrv(self, id):
        if id:
            user = self.getByIdSrv(id)
            result = self.query_service.delete(user[0]["id"])
            if result:
                return responseHttpUtils().response("Tokens to users deleting", None, None)
            return responseHttpUtils().response("Error deleting user tokens", None, None)
        else:
            return responseHttpUtils().response(None, None, result)
