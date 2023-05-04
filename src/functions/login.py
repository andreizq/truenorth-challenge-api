import bcrypt
from helpers.utils import util
from helpers.dbHelpers import users as userDB


def login(user):
    username = user.get("username")
    password = user.get("password")

    if not username or not password:
        return util.build_response(401, {"message": "username and password is required"})

    dynamoUser = userDB.get_user(username)
    if not dynamoUser or not dynamoUser.get("username"):
        return util.build_response(401, {"message": "Incorrect credentials"})

    if not bcrypt.checkpw(password.encode('utf-8'), dynamoUser.get("password").encode('utf-8')):
        return util.build_response(401, {"message": "Incorrect credentials"})

    userInfo = {
        "username": dynamoUser.get("username")
    }

    token = util.generate_token(userInfo)

    response = {
        "username": dynamoUser.get("username"),
        "balance": dynamoUser.get("balance"),
        "token": token
    }

    return util.build_response(200, response)
