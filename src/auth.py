import json
from functions.register import register
from functions.login import login
from helpers.utils import util

registerPath = "/register"
loginPath = "/login"


def handler(event, context):
    print(" Request Event : ", event)
    print(" Request Ctx : ", context)
    httpMethod = event["requestContext"]["http"]["method"]
    resource = event["requestContext"]["http"]["path"]
    requestBody = json.loads(event["body"])
    response = None
    if httpMethod == "POST" and resource == registerPath:
        response = register(requestBody)
    elif httpMethod == "POST" and resource == loginPath:
        response = login(requestBody)
    else:
        response = util.build_response(404, {"message": "404 Not Found "})
    return response
