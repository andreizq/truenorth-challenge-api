import json
import jwt
import os


def generate_token(userInfo):
    if not userInfo:
        return None
    return jwt.encode(userInfo, os.environ['JWT_SECRET'], algorithm='HS256')


def verify_token(token):
    try:
        decoded_token = jwt.decode(token, os.environ['JWT_SECRET'], algorithms=['HS256'])
        return (True, decoded_token['username'])
    except jwt.InvalidTokenError as e:
        print(str(e))
        return (False, None)


def build_response(status_code, body):
    return {
        'statusCode': status_code,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Credentials': True,
            'Content-Type': 'application/json',
        },
        'body': json.dumps(body, default=str),
    }
