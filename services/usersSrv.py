from middleware.responseHttpUtils import responseHttpUtils
from middleware.dateTimeUtils import dateTimeUtils
from repository.repoSQL import repoSQL
from middleware.hashPass import hash_password
from services.usersPersonalDataSrv import usersPersonalDataSrv
from services.usersRegistrationSrv import usersRegistrationSrv
from services.mailerSendSrv import mailerSendSrv
from middleware.randomCode import randomCode

class usersSrv():
    def __init__(self):
        self.query_service = repoSQL('users', ['id', 'firstname', 'lastname', 'email', 'phone', 'password', 'status'])
        self.users_personal_data_service = usersPersonalDataSrv()
        self.mailer_send_service = mailerSendSrv()
        self.users_registration_service = usersRegistrationSrv()
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

                if result:
                    self.users_personal_data_service.postSrv({
                        "user_id": result,
                        "sex": payload["sex"],
                        "address": payload["address"],
                        "date_of_birth": payload["date_of_birth"],
                        "country": payload["country"],
                        "city": payload["city"]
                    })
                    self.code = randomCode().generate()
                    self.mailer_send_service.sendSrv({
                        "email_from": payload["email"],
                        "subject": "Registration code",
                        "message": "Your registration code is: {}".format(self.code)
                    })
                    self.users_registration_service.postSrv({
                        "user_id": result,
                        "type": 1,
                        "code": self.code,
                        "status": False
                    })
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

            if result:
                self.users_personal_data_service.putSrv(id, {
                    "sex": payload["sex"],
                    "address": payload["address"],
                    "date_of_birth": payload["date_of_birth"],
                    "country": payload["country"],
                    "city": payload["city"]
                })
                return responseHttpUtils().response("User updated successfully", 200, result)
            else:
                return responseHttpUtils().response("Error updating user", 400, result)

    def forgotPasswordSrv(self, payload):
        if payload:
            result = self.query_service.get_by_conditions({
                "email": payload
            })
            if result and len(result) > 0 and result[0]["status"] == True:
                exists = self.users_registration_service.getByIdSrv(result[0]["id"], 2)
                self.code = randomCode().generate()
                self.mailer_send_service.sendSrv({
                    "email_from": result[0]["email"],
                    "subject": "Recovery code",
                    "message": "Your recovery code is: {}".format(self.code)
                })
                if exists and any(exist["status"] for exist in exists):
                    intime_expired_code = dateTimeUtils().getTime(exists[0]["createdat"])
                    if intime_expired_code is True:
                        self.users_registration_service.putSrv(exists[0]["id"], {
                            "user_id": result[0]["id"],
                            "type": 2,
                            "code": exists[0]["code"],
                            "status": False
                        })
                        return responseHttpUtils().response("Recovery code expired", 400)
                    return responseHttpUtils().response("The access code has been sent to your email", 200)
                self.users_registration_service.postSrv({
                    "user_id": result[0]["id"],
                    "type": 2,
                    "code": self.code,
                    "status": True
                })
            else:
                return responseHttpUtils().response("Email not found", 404)
            return responseHttpUtils().response("Code for recovery", 200)
        else:
            return responseHttpUtils().response("Email is required", 400)

    def changePasswordSrv(self, payload):
        if payload:
            result = self.query_service.get_by_conditions({
                "email": payload["email"]
            })
            if result and len(result) > 0:
                exists = self.users_registration_service.getByCodeSrv(2, payload["code"])
                if exists and any(exist["status"] for exist in exists):
                    intime_expired_code = dateTimeUtils().getTime(exists[0]["createdat"])
                    if intime_expired_code is False:
                        self.users_registration_service.putSrv(exists[0]["id"], {
                            "user_id": result[0]["id"],
                            "type": 2,
                            "code": payload["code"],
                            "status": False
                        })
                        user_data = {
                            "password": hash_password(payload["newpassword"])
                        }
                        response = self.query_service.update(result[0]["id"], user_data)
                        return responseHttpUtils().response("Recovery password changed", 200, response)
                    return responseHttpUtils().response("Recovery code expired", 400)
                else :
                    return responseHttpUtils().response("Recovery code not found", 404)
            else:
                return responseHttpUtils().response("Email not found", 404)

    def confirmRegistrationSrv(self, payload):
            if payload:
                result = self.query_service.get_by_conditions({
                    "email": payload["email"],
                    "status": True
                })
                if result and len(result) > 0:
                    exists = self.users_registration_service.getByCodeAndUserIdSrv(1, payload["code"], result[0]["id"])

                    if exists and bool(exist["status"] == False for exist in exists):
                        intime_expired_code = dateTimeUtils().getTime(exists[0]["createdat"])
                        if intime_expired_code is False and exists[0]["status"] == False:
                            response = self.users_registration_service.putSrv(exists[0]["id"], {
                                "user_id": result[0]["id"],
                                "type": 1,
                                "code": payload["code"],
                                "status": True
                            })
                            self.mailer_send_service.sendSrv({
                                "email_from": payload["email"],
                                "subject": "Registration success",
                                "message": "Your registration successfully confirmed"
                            })
                            return responseHttpUtils().response("Confirm registration success", 200, response)
                        return responseHttpUtils().response("Confirm registration code expired", 400)
                    else :
                        return responseHttpUtils().response("Confirm registration code not found", 404)
                else:
                    return responseHttpUtils().response("Email not found", 404)

    def deleteSrv(self, id):
        if id:
            result = self.query_service.delete(id)
            if result:
                return responseHttpUtils().response("User successfully deleted", 200)
            else:
                return responseHttpUtils().response("User deleted error", 400)