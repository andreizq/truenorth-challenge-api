import boto3
import json
from decimal import Decimal
from boto3.dynamodb.conditions import Key, Attr

# Set the region
session = boto3.session.Session()
dynamodb = session.resource('dynamodb', region_name="us-east-1")
operations_table = dynamodb.Table('operationsTable')
records_table = dynamodb.Table('recordsTable')


def get_operation(name):
    response = operations_table.get_item(
        Key={
            'id': name
        }
    )
    return response.get('Item')


def save_record(record):
    
    response = records_table.put_item(Item=record)
    return response['ResponseMetadata']['HTTPStatusCode'] == 200


def delete_record(recordId):
    response = records_table.update_item(
        Key={'id': recordId},
        UpdateExpression="set #isActive=:status",
        ExpressionAttributeValues={
            ':status': False},
        ExpressionAttributeNames={'#isActive': 'isActive'},
        ReturnValues="UPDATED_NEW")
    return response['ResponseMetadata']['HTTPStatusCode'] == 200


def get_records(username):
    params = {
        "IndexName": "UserIdIndex",
        "KeyConditionExpression": "#user_id = :user_id",
        "FilterExpression": "isActive = :isActive",
        "ExpressionAttributeNames": {"#user_id": "user_id"},
        "ExpressionAttributeValues": {":user_id": username, ":isActive": True},
        "ScanIndexForward": False,
        
    }

    response = records_table.query(**params)

    return response.get('Items')
