from app import create_app
import json
from flask import jsonify
from flask_swagger_ui import get_swaggerui_blueprint
from app.config import domain, port



app = create_app() # # Initialize

# # # DEFAULT ROUTE
@app.route('/')
def hello_world():
    return jsonify({'message': 'Hello, World!'}), 200


# =========================
# SWAGGER UI API MANGER
# =========================
SWAGGER_URL = '/api/ui'  # # URL for exposing Swagger UI

@app.route('/swagger-config') # # Serve Swagger configuration as a static route
def swagger_config():
    with open('static/swagger/config.json', 'r') as file:
        config_data = json.load(file)
    return jsonify(config_data)

swaggerui_bp = get_swaggerui_blueprint( # # Swagger UI blueprint
    SWAGGER_URL,  # URL where Swagger UI will be available
    f'http://{domain}:{port}/swagger-config',  # URL to the swagger config file
    config={
        'app_name': "Recipe API",
        "layout": "BaseLayout",
        "docExpansion": "none"
    }
)


# # Register the Swagger blueprint with the Flask app - (Mum recipe app)
app.register_blueprint(swaggerui_bp, url_prefix=SWAGGER_URL)


# # Excution entry point
if __name__ == '__main__':
	app.run(debug=True)
