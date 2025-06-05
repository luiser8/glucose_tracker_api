from middleware.responseHttpUtils import responseHttpUtils
from middleware.dateTimeUtils import dateTimeUtils
from repository.repoSQL import repoSQL
from middleware.hashPass import hash_password
from services.usersForgotSrv import usersForgotSrv
from services.mailerSendSrv import mailerSendSrv

class usersSrv():
    def __init__(self):
        self.query_service = repoSQL('users', ['id', 'firstname', 'lastname', 'email', 'phone', 'password', 'status'])
        self.query_service_personal_data = repoSQL('users_personal_data', ['id', 'user_id', 'sex', 'address', 'date_of_birth', 'country', 'city'])
        self.mailer_send_service = mailerSendSrv()
        self.users_forgot_service = usersForgotSrv()
        self.code = None

    def getAllSrv(self):
        response = self.query_service.get_all()
        if response:
            return responseHttpUtils().response("Users successfully", 200, response)
        else:
            return responseHttpUtils().response("Error listing users", 400, response)

    def getByIdSrv(self, id):
        response = self.query_service.get_by_id(id)
        if response:
            return responseHttpUtils().response("User by id successfully", 200, response)
        else:
            return responseHttpUtils().response("Error user not found", 404, response)

    def postSrv(self, payload):
        if payload:
            result = self.query_service.get_by_conditions({
                "email": payload["email"]
            })
            if result and len(result) > 0:
                return responseHttpUtils().response("Email already exists", 400, None)
            else:
                user_simple_data = {
                    "firstname": payload["firstname"],
                    "lastname": payload["lastname"],
                    "email": payload["email"],
                    "phone": payload["phone"],
                    "password": hash_password(payload["password"])
                }
                if "id" in payload:
                    user_simple_data["id"] = payload["id"]
                if "status" in payload:
                    user_simple_data["status"] = payload["status"]
                result = self.query_service.insert(user_simple_data)
                self.query_service_personal_data.insert({
                    "user_id": result,
                    "sex": payload["sex"],
                    "address": payload["address"],
                    "date_of_birth": payload["date_of_birth"],
                    "country": payload["country"],
                    "city": payload["city"]
                })
                if result:
                    return responseHttpUtils().response("User added successfully", 201, result)
                else:
                    return responseHttpUtils().response("Error adding user", 400, result)

    def putSrv(self, id, payload):
        if payload:
            user_simple_data = {
                "firstname": payload["firstname"],
                "lastname": payload["lastname"],
                "email": payload["email"],
                "phone": payload["phone"],
                "password": hash_password(payload["password"])
            }
            if "id" in payload:
                user_simple_data["id"] = payload["id"]
            if "status" in payload:
                user_simple_data["status"] = payload["status"]
            result = self.query_service.update(id, user_simple_data)
            self.query_service_personal_data.insert({
                "user_id": id,
                "sex": payload["sex"],
                "address": payload["address"],
                "date_of_birth": payload["date_of_birth"],
                "country": payload["country"],
                "city": payload["city"]
            })
            if result:
                return responseHttpUtils().response("User updated successfully", 200, result)
            else:
                return responseHttpUtils().response("Error updating user", 400, result)

    def forgotPasswordSrv(self, payload):
        if payload:
            result = self.query_service.get_by_conditions({
                "email": payload
            })
            if result and len(result) > 0 and result[0]["status"] == True:
                exists = self.users_forgot_service.getByIdSrv(result[0]["id"])
                self.code = self.mailer_send_service.sendSrv(result[0]["email"])
                if exists and any(exist["status"] for exist in exists):
                    intime_expired_code = dateTimeUtils().getTime(exists[0]["createdat"])
                    if intime_expired_code is True:
                        self.users_forgot_service.putSrv(exists[0]["id"], {
                            "user_id": result[0]["id"],
                            "code": exists[0]["code"],
                            "status": False
                        })
                        return responseHttpUtils().response("Recovery code expired", 400)
                    return responseHttpUtils().response("The access code has been sent to your email", 200)
                self.users_forgot_service.postSrv({
                    "user_id": result[0]["id"],
                    "code": self.code
                })
            else:
                return responseHttpUtils().response("Email not found", 404)
            return responseHttpUtils().response("Code for recovery", 200, self.code)
        else:
            return responseHttpUtils().response("Email is required", 400)

    def changePasswordSrv(self, payload):
        if payload:
            result = self.query_service.get_by_conditions({
                "email": payload["email"]
            })
            if result and len(result) > 0:
                exists = self.users_forgot_service.getByCodeSrv(payload["code"])
                if exists and any(exist["status"] for exist in exists):
                    intime_expired_code = dateTimeUtils().getTime(exists[0]["createdat"])
                    if intime_expired_code is False:
                        self.users_forgot_service.putSrv(exists[0]["id"], {
                            "user_id": result[0]["id"],
                            "code": payload["code"],
                            "status": False
                        })
                        user_data = {
                            "password": hash_password(payload["newpassword"])
                        }
                        self.query_service.update(result[0]["id"], user_data)
                        return responseHttpUtils().response("Recovery password changed", 200)
                    return responseHttpUtils().response("Recovery code expired", 400)
                else :
                    return responseHttpUtils().response("Recovery code not found", 404)
            else:
                return responseHttpUtils().response("Email not found", 404)

    def deleteSrv(self, id):
        if id:
            result = self.query_service.delete(id)
            if result:
                return responseHttpUtils().response("User successfully deleted", 200)
            else:
                return responseHttpUtils().response("User deleted error", 400)