import os, logging
from dotenv import load_dotenv


# =====================================
# Config Class (Flask App) - Parent
# =====================================
class Config:
    _instance = None # # Class attribute for singleton implementation

    def __init__(self):
            project_dir = os.path.join(os.path.dirname(__file__), os.pardir) # # Get and append our absolute project directory w.r.t OS container as a string
            dotenv_path = os.path.join(project_dir, '.env') # # Get and append the absolute or relative path ofr .env file to project path as string
            load_dotenv(dotenv_path) # # Load environment variables

            self.DOMAIN = os.getenv("DOMAIN", 'localhost') # # Get domain from .env file
            self.PORT = os.getenv("PORT", '5000') # # Get port from .env file
            self.PREFIX = os.getenv("PREFIX", '/api') # # Get prefix from .env file
            self.SECRET_KEY = os.getenv('SECRET_KEY', '%^$&123!@#') # # Get secret key fron .env file or default to provided
            self.SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///db.sqlite3') # # Get database url fron .env file or default to provided
            self.SQLALCHEMY_TRACK_MODIFICATIONS = False # # Help in memory caching
            self.JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', '#^%$*123!@#') # # Get JWT secret key fron .env file or default to provided

    @classmethod
    def get_instance(cls): # # Get the singleton instance of this very class
            if cls._instance is None: 
                cls._instance = Config() # # Create new instance if not created
            return cls._instance
    
    # # Getters methods for attributes
    def getDomain(self):
            return self.DOMAIN

    def getPort(self):
            return self.PORT

    def getPrefix(self):
            return self.PREFIX
    
    def getSecretKey(self):
         return self.SECRET_KEY
    
    def getSQLAlchemyUri(self):
         return self.SQLALCHEMY_DATABASE_URI
    
    def getSQLAlchemyTrackModifications(self):
         return self.SQLALCHEMY_TRACK_MODIFICATIONS
    
    def getJWTScretKey(self):
         return self.JWT_SECRET_KEY   

    @staticmethod
    def log_config(log_level=logging.INFO): # # Static method for logging config - INFO as default
        logging.basicConfig(
                level=log_level,
                filename="app.log",
                encoding="utf-8",
                filemode="a",
                format="{asctime} - {levelname} - {message}",
                style="{",
                datefmt="%Y-%m-%d %H:%M", )
        
        
# ================================
# Child Classes for Differ stages
# ================================
# # Development config
class DevelopmentConfig(Config):
    def __init__(self):
        super().__init__()
        self.DEBUG = os.getenv('DEBUG', True)  # Enable debug mode for development
    
# # Testing config
class TestingConfig(Config):
    def __init__(self):
        super().__init__()
        self.TESTING = os.getenv('TESTING', True) # # Get testing value default to true - for Testing stage
        self.SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI') # # In-memory database for testing

# # Production config
class ProductionConfig(Config):
    def __init__(self):
        super().__init__()        
        # Override DEV and TEST modes
        self.SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
        self.DEBUG = False
        self.TESTING = False


# # Fetch global config values
config_instance = Config.get_instance()
domain = config_instance.getDomain()
port = config_instance.getPort()
prefix = config_instance.getPrefix()