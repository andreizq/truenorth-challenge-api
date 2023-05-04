import bcrypt
from helpers.utils import util
from helpers.dbHelpers import users as userDB


def register(userInfo):
    username = userInfo.get("username")
    password = userInfo.get("password")
    balance = userInfo.get("balance")

    if not username or not password or not balance:
        return util.build_response(401, {"message": "Username, password and balance are required"})

    dynamoUser = userDB.get_user(username)
    if dynamoUser and dynamoUser.get("username"):
        return util.build_response(401, {"message": "User already exists"})

    encryptedPassword = bcrypt.hashpw(password.strip().encode('utf-8'), bcrypt.gensalt())
    user = {
        "username": username.lower(),
        "password": encryptedPassword.decode('utf-8'),
        "balance": balance
    }

    savedUserResponse = userDB.save_user(user)
    if not savedUserResponse:
        return util.build_response(503, {"message": "server error"})

    return util.build_response(200, {"username": username, "balance": balance})
