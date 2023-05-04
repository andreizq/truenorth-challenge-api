from helpers.utils import util
from helpers.dbHelpers import operations as operationDB


def deleteRecord(recordId):

	records = operationDB.delete_record(recordId)

	return util.build_response(200, records)