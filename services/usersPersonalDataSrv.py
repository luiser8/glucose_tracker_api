from repository.repoSQL import repoSQL
from middleware.responseHttpUtils import responseHttpUtils

class usersPersonalDataSrv():
    def __init__(self):
        self.result = None
        self.query_service = repoSQL('users_personal_data', ['id', 'user_id', 'phone', 'sex', 'address', 'date_of_birth', 'country', 'city'])

    def getByIdSrv(self, id):
        response = self.query_service.get_by_id(id)
        return responseHttpUtils().response(None, None, response)

    def getByUserIdSrv(self, user_id):
        response = self.query_service.get_by_conditions({
            "user_id": user_id
        })
        return responseHttpUtils().response(None, None, response)

    def postSrv(self, payload):
        if not payload:
            return responseHttpUtils().response("Payload is required", None, None)

        user_data = {
            "user_id": payload["user_id"],
            "phone": payload["phone"],
            "sex": payload["sex"],
            "address": payload["address"],
            "date_of_birth": payload["date_of_birth"],
            "country": payload["country"],
            "city": payload["city"]
        }

        user_personal_data_exists = self.getByUserIdSrv(payload["user_id"])

        if user_personal_data_exists:
            return responseHttpUtils().response("User personal data ID match stored user", None, None)
        else:
            self.result = self.query_service.insert(user_data)

        return self.result

    def putSrv(self, user_id, payload):
        if not payload:
            return responseHttpUtils().response("Payload is required", None, None)

        user_data = {
            "user_id": user_id,
            "phone": payload["phone"],
            "sex": payload["sex"],
            "address": payload["address"],
            "date_of_birth": payload["date_of_birth"],
            "country": payload["country"],
            "city": payload["city"]
        }
        if id:
            user_data["user_id"] = user_id
        if "status" in payload:
            user_data["status"] = payload["status"]

        user = self.getByUserIdSrv(user_id)
        self.result = self.query_service.update(user[0]["id"], user_data)

        if self.result:
            return responseHttpUtils().response(None, None, self.result)
        return responseHttpUtils().response("User personal data error updating", None, None)
