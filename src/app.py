import json
from functions.createRecord import createRecord
from functions.deleteRecord import deleteRecord
from functions.getRecords import getRecords
from helpers.utils import util


def handler(event, context):
    httpMethod = event["requestContext"]["http"]["method"]
    authorization = event["headers"].get("authorization")
    print(event)
    response = None
    
    if authorization:
        token = authorization.split()[1]
        (verified, username) = util.verify_token(token)

        if verified:
            if httpMethod == "POST":
                requestBody = json.loads(event["body"])
                response = createRecord(requestBody, username)
            elif httpMethod == "DELETE":
                recordId = event["pathParameters"]["id"]
                response = deleteRecord(recordId)
            elif httpMethod == "GET":
                response = getRecords(username)
            else:
                response = util.build_response(404, {"message": "404 Not Found "})
        else:
            response = util.build_response(401, {"message": "Invalid authorization token"})
    else:
        response = util.build_response(401, {"message": "Invalid authorization token"})

    return response
