from flask import jsonify


# =================================================
# Custom Error Handler - Specific Exception (Class)
# =================================================
class AppException(Exception): 
	def __init__(self, message, status_code): # # When instantited, should be passed with this initializer variables
		self.message = message
		self.status_code = status_code
	

# # Handles application exceptions
def handle_application_error(e):  # # Business logic handler
	response = {
		'error': {
			'message': e.message,
			'status_code': e.status_code
			}
	}
	return jsonify(response), e.status_code

# # Handle http exceptions
def handle_http_exception(e): # # Server error handler
	response = {
		'error': {
			'message': e.description,
			'status_code': e.code
			}
	}
	return jsonify(response), e.code

# # Handle generic exceptions - catch all handler for unexpected errors
def handle_generic_exception(e):
	response = {
		'error': {
			'message': 'An unexpected error occured.',
			'status_code': 500
			}
	}
	return jsonify(response), 500
