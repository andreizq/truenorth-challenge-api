import uuid
import requests
from time import time
from datetime import datetime
from math import sqrt
from helpers.utils import util
from decimal import Decimal
from helpers.dbHelpers import operations as operationDB
from helpers.dbHelpers import users as userDB


def createRecord(recordInfo, username):
	operationId = recordInfo.get("operation")
	value1 = recordInfo.get("value1")
	value2 = recordInfo.get("value2")
	result = None

	operation = operationDB.get_operation(operationId)
	dynamoUser = userDB.get_user(username)

	cost = operation.get("cost")
	balance = Decimal(dynamoUser.get("balance"))

	balance = balance - cost

	if balance < 0:
		return util.build_response(403,{"message": "Insufficient balance"} )

	if operationId == "add":
		result = value1 + value2
	elif operationId == "subst":
		result = value1 - value2
	elif operationId == "mult":
		result = value1 * value2
	elif operationId == "div":
		if value2 == 0:
			return util.build_response(400,{"message": "Dividend can't be 0"} )
		result = str(value1 / value2)
	elif operationId == "sqrt":
		if value1 < 0:
			return util.build_response(400,{"message": "Square root can't have a negative parameter"})
		result = str(sqrt(value1))
	elif operationId == "rndstr":
		if value1 < 1 or value1 > 20:
			return util.build_response(400, {"message": "Random string length has to be between 1 and 20"})
		response = requests.get('https://www.random.org/strings/?num=1&len=' + str(value1) + '&digits=on&upperalpha=on&loweralpha=on&unique=on&format=plain&rnd=new')  # noqa: E501
		result = response.text
	else:
		return util.build_response(400, {"message": "Invalid operation"})

	# save record
	id_db = uuid.uuid4()
	record = {
		"id": str(id_db),
		"operation_id": operationId,
		"user_id": username,
		"cost": cost,
		"user_balance": balance,
		"operation_response": str(result),
		"date": int(time()),
		"timestamp": str(datetime.now()),
		"isActive": True
	}

	userDB.update_user({"username": username, "balance": str(balance)})
	dbRes = operationDB.save_record(record)

	if not dbRes:
		return util.build_response(503, {"message": "server error"})

	return util.build_response(200, record)
