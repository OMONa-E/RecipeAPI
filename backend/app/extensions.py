from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask import current_app


# # Instantiate the extensions
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

current_app.logger.info(f'Extensions instantiated successfully')