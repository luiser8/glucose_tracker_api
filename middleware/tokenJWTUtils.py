import jwt
import datetime
import os
from middleware.hashPass import decode_token

class tokenJWTUtils():
    def __init__(self):
        self.secret_key = os.getenv("SECRET_KEY")
        self.secret_key_algorithm = os.getenv("ALGORITHM")
        self.expires_in = int(os.getenv("EXPIRES_IN"))

    def getTokenUserId(self, headers):
        if "Authorization" in headers:
            token = headers["Authorization"].split()[1]
            token_decode = decode_token(token)
            return { "user_id": token_decode["id"], "decoded_token": token_decode }

    def generate(self, payload):
        access_token = jwt.encode({
            "id": payload[0]["id"],
            "firstname": payload[0]["firstname"],
            "lastname": payload[0]["lastname"],
            "email": payload[0]["email"],
            "phone": payload[0]["phone"],
            "status": payload[0]["status"],
            "sex": payload[0]["sex"],
            "address": payload[0]["address"],
            "date_of_birth": payload[0]["date_of_birth"],
            "country": payload[0]["country"],
            "city": payload[0]["city"],
            "exp": (datetime.datetime.now() + datetime.timedelta(minutes=self.expires_in)).timestamp()
        }, self.secret_key, self.secret_key_algorithm)

        refresh_token = jwt.encode({
            "id": payload[0]["id"],
            "firstname": payload[0]["firstname"],
            "lastname": payload[0]["lastname"],
            "email": payload[0]["email"],
            "phone": payload[0]["phone"],
            "status": payload[0]["status"],
            "sex": payload[0]["sex"],
            "address": payload[0]["address"],
            "date_of_birth": payload[0]["date_of_birth"],
            "country": payload[0]["country"],
            "city": payload[0]["city"],
            "exp": (datetime.datetime.now() + datetime.timedelta(minutes=self.expires_in * 7)).timestamp()
        }, self.secret_key, self.secret_key_algorithm)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }