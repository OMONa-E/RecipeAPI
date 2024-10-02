from functools import wraps
from flask import current_app
from flask_restful import Resource
from flask_jwt_extended import get_jwt, create_access_token, jwt_required, get_jwt_identity
from .utils import user_parser, serializeJsonToString
from .exceptions import AppException
from .models import User, BlacklistToken
from .extensions import db



# ==============================================
# Role Based Access Control  (RBAC) - Decorator
# ==============================================
def role_required(role): # # Creates decorator/annotation function
	def decorator(fn):
		@wraps(fn)
		@jwt_required()
		def wrapper(*args, **kwargs):
			user_id = get_jwt_identity() # # Gets specific user JSONWEB Token
			user = User.query.get_or_404(user_id) # # Retrieve and validates as well

			if not user or user.role != role: # # Validates the user, role and raises exception otherwise
				current_app.logger.info(f'User {user_id} attempting to access services not allowed for the user')
				raise AppException("Forbidden: You do not have permission on this previllege.", 403)
			return fn(*args, **kwargs)
		return wrapper
	return decorator


# ============================================
# Authorization and Authentication Resources
# ============================================

class Signup(Resource): # # Signup resource
	def post(self):
		parser = user_parser() 
		data = parser.parse_args() # Parsing all data provided by the client

		current_app.logger.info(f'Client attempting to singup')

		username = data['username']
		password = data['password']
		role = data.get('role', 'USER').upper() 
		# # Serializing our specific data
		allergies = serializeJsonToString(data['allergies'])
		dislikes = serializeJsonToString(data['dislikes'])
		hard_to_get = serializeJsonToString(data['hard_to_get'])

		if not role: # # Validate if role is null and assign default
			role = 'USER'
		
		if not username or not password: # # Validate username and password
			current_app.logger.info(f'Client failed to provide username or password')
			raise AppException('Username and Password are required', 400)
		
		user = User.query.filter_by(username=username).first() # # Retrieve the first user by username
		if user: # # Validate if user is present
			current_app.logger.info(f'Client creating account with exiting username crendiential')
			raise AppException('User already exists', 400)
		
		new_user = User( # # create a new user object
						username=username, 
						role=role.upper(),
						allergies=allergies,
						dislikes=dislikes,
						hard_to_get=hard_to_get,
						family_size=data['family_size'],
						aveg_intake_person=data['aveg_intake_person']
		)
		new_user.set_password(password) # # Set the new user password as a hash format 
		db.session.add(new_user) # # Add the the user to the open database session 
		db.session.commit() # # Save and flush the session	
		current_app.logger.info(f'Client {username} created an account successfully')	
		return {'message': f'User {username} created successfully'}, 201


class Login(Resource): # # Login resource
	def post(self):
		parser = user_parser() # # Call the user parser function
		data = parser.parse_args() # # Parse all the client data
		# # Assign the parsed data 
		username = data['username']
		password = data['password']

		current_app.logger.info(f'Client attempting to login')

		if not username or not password: # # Validate client username and password
			current_app.logger.info(f'Client did not provide username or password')
			raise AppException('Username and password are required', 400)
		
		user = User.query.filter_by(username=username).first() # # Retrieve the first user by username
		if not user or not user.check_password(password): # # Validate user and checks provided password against hashed password
			current_app.logger.info(f'Client provided wrong username or password ')
			raise AppException('Invalid username or password', 401)
		
		access_token = create_access_token(identity=user.id) # # create JWT token
		current_app.logger.info(f'Client logged in successfully')
		return {'access_token': access_token}, 200
	

class UpdateUserProfile(Resource): # # User update resource
	@jwt_required() # # Annotates the method to authorized and authenticated clients
	def put(self):
		parser = user_parser() # # Parses client arguments
		data = parser.parse_args()
		user_id = get_jwt_identity() # # Gets the present user JSON token
		user = User.query.get_or_404(user_id) # # Retrieve user by the JSON Token and throws exception if not

		current_app.logger.info(f'User {user_id} attempting to update user profile')

		if user.id != user_id: # # Validate user id
			current_app.logger.info(f'User {user_id} is not the profile owner')
			raise AppException('You do not have permission to update this this user', 403)

		# # Validate the client provided data/arguments 
		if 'username' in data:
			user.username = data['username']
		if 'password' in data:
			user.password = data['password']
		if 'role' in data:
			user.role = data['role']
		if 'allergies' in data:
			user.allergies = serializeJsonToString(data['allergies'])
		if 'dislikes' in data:
			user.dislikes = serializeJsonToString(data['dislikes'])
		if 'hard_to_get' in data:
			user.hard_to_get = serializeJsonToString(data['hard_to_get'])
		if 'family_size' in data:
			user.family_size = data['family_size']
		if 'aveg_intake_person' in data:
			user.aveg_intake_person = data['aveg_intake_person']

		db.session.commit() # # Save and flush the passed validation data
		current_app.logger.info(f'User {user_id} upadted the profile successfully')
		return {'message': 'Profile updated successfully', 'user': user.to_dict()}, 200	


class Logout(Resource): # # Logout resource
	@jwt_required() # # Require when logged in
	def post(self):
		jti = get_jwt()["jti"]  # # Get the JWT ID (JTI) from the token

		current_app.logger.info(f'Attempting to logout')
		
		if not jti: # # Validate if the JWT ID is valid (not empty)
			current_app.logger.info(f'JTI was not found')
			raise AppException("Invalid token: no JTI found", 400)
		
		if BlacklistToken.query.filter_by(token=jti).first(): # # Validate if the token is already blacklisted
			current_app.logger.info(f'The JTI was black listed already')
			raise AppException("Token has already been blacklisted", 400)
		
		blacklisted_token = BlacklistToken(token=jti)

		db.session.add(blacklisted_token)
		db.session.commit()		
		current_app.logger.info(f'The JTI was black listed successfully')
		return {"message": "Successfully logged out"}, 200


class DeleteUser(Resource): # # Delete user resource
	@jwt_required() # # Require logged in
	def delete(self):
		user_id = get_jwt_identity()
		user = User.query.get_or_404(user_id)

		current_app.logger.info(f'User {user_id} attempting to delete {user.username}')

		if user.id != user_id: # # Validate user
			current_app.logger.info(f'User {user_id} has no ownership to this account')
			raise AppException('You dont have permission to delete this account', 403)

		db.session.delete(user)
		db.session.commit()
		current_app.logger.info(f'User {user_id} deleted {user.username} account successfully')
		return {'message': f'User {user.username} deleted successfully'}, 200


class DeleteUserById(Resource): # # Delete by id user resource
	@role_required('SUPERADMIN')
	def delete(self, user_id):
		user = User.query.get_or_404(user_id) # # Get user by id

		if user.role != 'SUPERADMIN': # # Validate user role 
			current_app.logger.info(f'User {user.id} has no SuperAdmin role')
			raise AppException('Accounts can only be deleted by the superadmin.', 403)
		
		db.session.delete(user)
		db.session.commit()
		current_app.logger.info(f'Account {user.username} deleted successfully')
		return {'message': f'User {user.username} deleted successfully'}, 200
