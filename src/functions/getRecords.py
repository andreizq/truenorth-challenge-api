from helpers.utils import util
from helpers.dbHelpers import operations as operationDB


def getRecords(username):

	res = operationDB.get_records(username)

	return util.build_response(200, res)
