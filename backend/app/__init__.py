from flask import Flask
from flask_cors import CORS
from werkzeug.exceptions import HTTPException
from .config import DevelopmentConfig
from .exceptions import AppException, handle_application_error, handle_http_exception, handle_generic_exception
from .models import BlacklistToken
from .extensions import db, jwt, migrate



# =================
# Define Flask app
# =================
def create_app():
	app = Flask(__name__, static_folder='/static')
	CORS(app) # # Enable Cross-Origin Resource Sharing
	
	# # Load configuration from the config file
	app.config.from_object(DevelopmentConfig())

	# # Set up logging
	DevelopmentConfig.log_config()
	
	# # Initialize extensions
	db.init_app(app)
	migrate.init_app(app, db)
	jwt.init_app(app)

	
    # # Token Blacklist Loader
	@jwt.token_in_blocklist_loader
	def check_if_token_in_blacklist(jwt_header, jwt_payload):
		jti = jwt_payload['jti']  # # Get the unique identifier for the JWT (jti)
        # # Check if the token is in the BlacklistToken table
		blacklisted_token = BlacklistToken.query.filter_by(token=jti).first() 
		return bool(blacklisted_token)  #  # Return True if the token is blacklisted
	

	# # Register blueprints w.t routes
	from app.routes import api_blueprint
	app.register_blueprint(api_blueprint, url_prefix='/api')
	
	# # register error handlers with appropriate Exception classes
	app.register_error_handler(AppException, handle_application_error)
	app.register_error_handler(HTTPException, handle_http_exception)
	app.register_error_handler(Exception, handle_generic_exception)
	
	return app
