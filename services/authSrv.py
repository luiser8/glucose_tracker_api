import os
from middleware.tokenJWTUtils import tokenJWTUtils
from middleware.responseHttpUtils import responseHttpUtils
from repository.repoSQL import repoSQL
from middleware.hashPass import hash_password
from services.usersAuth import usersAuthSrv
from services.usersRegistrationSrv import usersRegistrationSrv

class authSrv:
    def __init__(self):
        self.secret_key = os.getenv("SECRET_KEY")
        self.secret_key_algorithm = os.getenv("ALGORITHM")
        self.expires_in = int(os.getenv("EXPIRES_IN"))
        self.query_service = repoSQL('users', ['id', 'email', 'phone', 'firstname', 'lastname', 'status', 'sex', 'address', 'date_of_birth', 'country', 'city'])
        self.users_auth_service = usersAuthSrv()
        self.generate_token = tokenJWTUtils()
        self.users_registration_service = usersRegistrationSrv()

    def loginSrv(self, payload):
        if payload:
            result = self.query_service.get_with_joins(
                joins=[{
                    'table': 'users_personal_data',
                    'on': {'users.id': 'users_personal_data.user_id'}
                }],
                select_columns=[
                    'users.id', 'users.email', 'users.firstname',
                    'users.lastname', 'users.status', 'users_personal_data.photo',
                    'users_personal_data.phone', 'users_personal_data.sex',
                    'users_personal_data.address', 'users_personal_data.date_of_birth',
                    'users_personal_data.country', 'users_personal_data.city'
                ],
                conditions={
                    'users.email': payload["email"],
                    'users.password': hash_password(payload["password"])
                }
            )
            if result:
                user_registration = self.users_registration_service.getByIdSrv(result[0]["id"], 1)
                if result[0]["status"] == False:
                    return responseHttpUtils().response("User is inactive", 403, None)
                if user_registration[0]["status"] == False:
                    return responseHttpUtils().response("User registration not activate", 403, None)
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
            result = self.query_service.get_with_joins(
                joins=[{
                    'table': 'users_personal_data',
                    'on': {'users.id': 'users_personal_data.user_id'}
                }],
                select_columns=[
                    'users.id', 'users.email', 'users.firstname',
                    'users.lastname', 'users.status', 'users_personal_data.photo',
                    'users_personal_data.phone', 'users_personal_data.sex',
                    'users_personal_data.address', 'users_personal_data.date_of_birth',
                    'users_personal_data.country', 'users_personal_data.city'
                ],
                conditions={
                    'users.id': user_id
                }
            )
            if result:
                user_registration = self.users_registration_service.getByIdSrv(result[0]["id"], 1)
                if result[0]["status"] == False:
                    return responseHttpUtils().response("User is inactive", 403, None)
                if user_registration[0]["status"] == False:
                    return responseHttpUtils().response("User registration not activate", 403, None)
                tokens = self.generate_token.generate(result)
                if tokens and result:
                    self.users_auth_service.postSrv({
                        "user_id": result[0]["id"],
                        "access_token": tokens["access_token"],
                        "refresh_token": tokens["refresh_token"]
                    })
                return responseHttpUtils().response("Token refresh for auth", 200, tokens)