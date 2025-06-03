import os
from middleware.tokenJWTUtils import tokenJWTUtils
from middleware.responseHttpUtils import responseHttpUtils
from repository.repoSQL import repoSQL
from middleware.hashPass import hash_password
from services.usersAuth import usersAuthSrv

class authSrv:
    def __init__(self):
        self.secret_key = os.getenv("SECRET_KEY")
        self.secret_key_algorithm = os.getenv("ALGORITHM")
        self.expires_in = int(os.getenv("EXPIRES_IN"))
        self.query_service = repoSQL('users', ['id', 'email', 'firstname', 'lastname', 'status'])
        self.users_auth_service = usersAuthSrv()
        self.generate_token = tokenJWTUtils()

    def loginSrv(self, payload):
        if payload:
            email = payload["email"]
            password = hash_password(payload["password"])
            result = self.query_service.get_by_conditions({
                "email": email,
                "password": password
            })
            if result:
                if result[0]["status"] == False:
                    return responseHttpUtils().response("User is inactive", 403, None)
                tokens = self.generate_token.generate(result)
                if tokens and result:
                    self.users_auth_service.postSrv({
                        "user_id": result[0]["id"],
                        "access_token": tokens["access_token"],
                        "refresh_token": tokens["refresh_token"]
                    })
                    return responseHttpUtils().response("Token for auth", 200, tokens)
            else:
                return responseHttpUtils().response("User not found", 401)

    def destroySrv(self, user_id):
        if user_id:
            response = self.users_auth_service.deleteSrv(user_id)
            return responseHttpUtils().response("Tokens destroy", 200, response)

    def refreshSrv(self, user_id):
        if user_id:
            result = self.query_service.get_by_id(user_id)
            if result:
                if result[0]["status"] == False:
                    return responseHttpUtils().response("User is inactive", 403, None)
                tokens = self.generate_token.generate(result)
                if tokens and result:
                    self.users_auth_service.postSrv({
                        "user_id": result[0]["id"],
                        "access_token": tokens["access_token"],
                        "refresh_token": tokens["refresh_token"]
                    })
                return responseHttpUtils().response("Token refresh for auth", 200, tokens)