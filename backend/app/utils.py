from flask_restful import reqparse
import json


# ========================================
# Request Parser (for POST/PUT requests)
# ========================================
# # Function for user-related arguments
def user_parser():
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help='Username must be a string and cannot be blank')
    parser.add_argument('password', type=str, required=True, help='Password must be a string and cannot be blank')
    parser.add_argument('role', type=str, help='Role must be a string')
    parser.add_argument('allergies', type=str, action='append', help='Allergies must be a string')
    parser.add_argument('dislikes', type=str, action='append', help='Dislikes must be a string')
    parser.add_argument('hard_to_get', type=str, action='append', help='Hard to get must be a string')
    parser.add_argument('family_size', type=int, help='Family size must be an integer')
    parser.add_argument('aveg_intake_person', type=int, help='Average intake per person must be an integer')
    return parser

def user_update_parser():
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, help='Username must be a string and cannot be blank')
    parser.add_argument('password', type=str, help='Password must be a string and cannot be blank')
    parser.add_argument('role', type=str, help='Role must be a string')
    parser.add_argument('allergies', type=str, action='append', help='Allergies must be a string')
    parser.add_argument('dislikes', type=str, action='append', help='Dislikes must be a string')
    parser.add_argument('hard_to_get', type=str, action='append', help='Hard to get must be a string')
    parser.add_argument('family_size', type=int, help='Family size must be an integer')
    parser.add_argument('aveg_intake_person', type=int, help='Average intake per person must be an integer')
    return parser

# Function for recipe-related arguments
def recipe_parser():
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True, help='Recipe name cannot be blank')
    parser.add_argument('ingredients', type=str, required=True, help='Ingredients cannot be blank')
    parser.add_argument('instructions', type=str, required=True, help='Instructions cannot be blank')
    parser.add_argument('category', type=str, help='Recipe category')
    return parser


# ======================================================
# Serialization and De-serialization (Database records)
# ======================================================
def safe_json_load(data):
    try:
        return json.loads(data)
    except (TypeError, ValueError):
        return data  # # If not JSON, return the original data


def serializeJsonToString(JSON_str):
    if isinstance(JSON_str, list) or isinstance(JSON_str, dict) or isinstance(JSON_str, tuple) or isinstance(JSON_str, set):
            JSON_str = json.dumps(JSON_str)  # # Convert to JSON string
    return JSON_str


def deserializeStringToJson(str_JSON):
    if str_JSON:
        try:
            str_JSON = json.loads(str_JSON) # # Convert JSON back to original string
        except json.JSONDecodeError:
            pass  # # content is a regular string not JSON-encoded
    return str_JSON
    