from flask import jsonify
from flask_api import status

# create your validations here.

# fetch count error.
def fetchcount_error(records_length: str):
    return jsonify(
        {
            'status_code': status.HTTP_400_BAD_REQUEST, 
            'success': False,
            'message': 'fetchcount should be !0 | <= '+str(records_length), 
        }
    )

# sort error.
def sortorder_error():
    return jsonify(
        {
            'status_code': status.HTTP_400_BAD_REQUEST, 
            'success': False,
            'message': 'sortorder should be only ASC|DESC !', 
        }
    )

# internal server error.
def ISE():
    return jsonify(
        {
            'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR, 
            'success': False,
            'message': 'Internal server error', 
        }
    )

# server error if no data found.
def server_error():
    return jsonify(
        {
            'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR, 
            'success': False,
            'message': 'Error from server', 
        }
    )

# result not found error.
def notfound_error():
    return jsonify(
        {
            'status_code': status.HTTP_404_NOT_FOUND, 
            'success': False,
            'message': 'Not found!', 
        }
    )

# bad request error.
def badreq_error(msg: str):
    return jsonify(
        {
            'status_code': status.HTTP_400_BAD_REQUEST, 
            'success': False,
            'message': msg, 
        }
    )

    