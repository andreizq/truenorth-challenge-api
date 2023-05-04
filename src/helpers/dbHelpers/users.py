import boto3

# Set the region
session = boto3.session.Session()
dynamodb = session.resource('dynamodb', region_name="us-east-1")
user_table = dynamodb.Table('usersTable')


def get_user(username):
    response = user_table.get_item(
        Key={
            'username': username
        }
    )
    return response.get('Item')


def save_user(user):
    response = user_table.put_item(Item=user)
    return response['ResponseMetadata']['HTTPStatusCode'] == 200


def update_user(user):
    response = user_table.update_item(
        Key={'username': user["username"]},
        UpdateExpression="set #balance=:b",
        ExpressionAttributeValues={
            ':b': user["balance"]},
        ExpressionAttributeNames={'#balance': 'balance'},
        ReturnValues="UPDATED_NEW")
    return response['ResponseMetadata']['HTTPStatusCode'] == 200
