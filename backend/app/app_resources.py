import random
from datetime import datetime, timedelta
from flask import current_app
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from .auth_resources import role_required
from .models import Recipe, Pin, RecipePlan
from .utils import recipe_parser, serializeJsonToString
from .exceptions import AppException
from .extensions import db
from sqlalchemy import func



# =========================================
# API Resources Classes: (CRUD Operations)
# =========================================

# ======================= #
# Recipe Resource classes #

class RecipeGetAll(Resource): # # Retrieve all recipe from the database
	@jwt_required() # # Requires client auth
	def get(self):
		recipes = Recipe.query.all()
		return [recipe.to_dict() for recipe in recipes], 200



class RecipeGetById(Resource): # # Retrieve recipe by Id
	@jwt_required()		# # Any user logged in can view a specific recipe
	def get(self, recipe_id):
		recipe = Recipe.query.get_or_404(recipe_id)
		return recipe.to_dict(), 200



class RecipeCreate(Resource): # # Create a recipe
	@role_required('ADMIN') # # Require client to be an ADMIN ROLE
	def post(self):
		parser = recipe_parser() # # Parses client data
		data = parser.parse_args()
		name = data['name']
		ingredients = serializeJsonToString(data['ingredients'])
		instructions = serializeJsonToString(data['instructions']) # # Serialize the JSON		
		user_id = get_jwt_identity() # # Get client JWT Id

		# # Log data creation event
		current_app.logger.info(f'User {user_id} attempting to create recipe: {data['name']}')

		# # Validate none null client data
		if not name or not ingredients or not instructions:
			current_app.logger.info(f'User {user_id} failed to provide required fields fro recipe creation')
			raise AppException(f'Name, ingredients and instructions fields cannot be blank', 400)

		# # Instantiate a new recipe object
		recipe = Recipe(
			name=name,			
			instructions=instructions,
			category=data['category'],
			# # TODO: amount to be serve
			ingredients=ingredients,
			created_by=user_id
		)		
		recipe.calculate_total_cost(ingredients=ingredients) # # Sets the total cost for ingredients
		current_app.logger.info(f'Total cost for recipe {name} calculated sucdessfully.')

		db.session.add(recipe) # # Add new object to database session
		db.session.commit() # # Save and flush the transaction
		current_app.logger.info(f'Recipe {name} created successfully by user {user_id}')
		return {'message': 'Recipe created sucessfully', "recipe": recipe.to_dict()}, 201



class RecipeUpdateById(Resource): # # Upadate a recipe by Id
	@role_required('ADMIN') # # Requires ADMIN ROLE
	def put(self, recipe_id):
		recipe = Recipe.query.get_or_404(recipe_id) # # Retrieve recipe by Id
		user_id = get_jwt_identity() # # Gets current user JSONWEB Token
		
		current_app.logger.info(f'User {user_id} attempting to update recipe {recipe.name}')

		if recipe.created_by != user_id: # # Validate against the recipe created_by field
			current_app.logger.info(f'User {user_id} did not create the recipe {recipe.name}')
			raise AppException('You do not have permission to update this recipe', 403)

		parser = recipe_parser() # # Parses the client provided data
		data = parser.parse_args()
		
		# # Validate each data field
		if 'name' in data:
			recipe.name = data['name']
		if 'ingredients' in data:
			recipe.ingredients = data['ingredients']
		if 'instructions' in data:
			recipe.instructions = serializeJsonToString(data['instructions'])
		if 'category' in data:
			recipe.category = data['category']
		# # TODO
		# if 'amount_to_serve' in data:
		# 	recipe.amount_to_serve = data['amount_to_serve']

		db.session.commit() # # Save and flush the changes
		current_app.logger.info(f'User {user_id} updated recipe {recipe.name} successfully')
		return {'message': 'Recipe updated sucessfully', "recipe": recipe.to_dict()}, 200



class RecipeDeleteById(Resource): # # Delete a recipe by Id
	@role_required('ADMIN') # # Requires ADMIN ROLE
	def delete(self, recipe_id): 
		recipe = Recipe.query.get_or_404(recipe_id) # # Retrieve a recipe by Id or throws an exception otherwise
		user_id = get_jwt_identity() # # Gets tee current user JWTWEB Token

		current_app.logger.info(f'User {user_id} attempting to delete recipe {recipe.name}')

		if recipe.created_by != user_id: # # Validate client against created_by field
			current_app.logger.info(f'User {user_id} did not create the recipe {recipe.name}')
			raise AppException('You do not have permission to delete this recipe.', 403)

		db.session.delete(recipe) # # Delete a recipe and associated pins
		db.session.commit() # # Save and flush the changes
		current_app.logger.info(f'User {user_id} deleted recipe {recipe.name} successfully')
		return {'message': 'Recipe deleted sucessfully'}, 200


# ============================== #
# Pin (Comment) Resource classes #

class PinCreate(Resource): # # Create a pin
	@jwt_required() # # Requires logged in user
	def post(self, recipe_id):
		recipe = Recipe.query.get_or_404(recipe_id) # # Retrieve a recipe by Id - provide by the client otherwise throws 404 exception 
		user_id = get_jwt_identity() # # Gets the current user JWTWEB Token

		current_app.logger.info(f'User {user_id} attempting to pin recipe {recipe.name}')

		parser = reqparse.RequestParser() # # Intialize the parser
		parser.add_argument('content', type=str, required=True, help='Content cannot be blank') # # Register/add argument to be parse
		data = parser.parse_args() # # Parse the client data

		if not data['content']:
			current_app.logger.info(f'User {user_id} did not provide content field')
			raise AppException('Content field cannot be null', 403)

		pin = Pin( # # Instantiate a pin object and its associated attributes
			recipe_id=recipe_id,
			user_id=user_id,
			content=data['content']
		)
		db.session.add(pin) # # Add the pin to the database session
		db.session.commit() # # Save and flush the changes
		current_app.logger.info(f'User {user_id} created pin for recipe {recipe.name} successfully')
		return {'message': 'Pin/Comment added successfully', 'pin': pin.to_dict()}, 201



class PinGetByRecipeId(Resource): # # Retrieve all pin/comment by id for a recipe
	@jwt_required()
	def get(self, recipe_id):
		pins = Pin.query.filter_by(recipe_id=recipe_id).all() # # Retrieve all pins in the database associated with the recipe identified by its Id
		return [pin.to_dict() for pin in pins]



# ========================== #
# Recipe Plan Resource class #
class GetRecipePlan(Resource):
	@jwt_required() # # Loggin previllege
	def get(self):
		user_id = get_jwt_identity()

		current_app.logger.info(f'User {user_id} attempting to retrieve recipe plan')

		# # Retrieve recipes user has had in the last 10days
		ten_days_ago = datetime.now() - timedelta(days=5)
		recent_recipe_plans = RecipePlan.query.filter(
			RecipePlan.user_id == user_id,
			RecipePlan.date >= ten_days_ago
		).all()

		if not recent_recipe_plans: # # Validate recipe plan
			current_app.logger.info(f'User {user_id} had no recipe plan before')
		else:
			current_app.logger.info(f'User {user_id} already has recipe plan within the last 5 days')

		# # List of recipe ids from recipe plan
		recent_recipe_ids = [plan.recipe_id for plan in recent_recipe_plans]

		# # Retrive today's plan
		today = datetime.now().date()
		today_plan = RecipePlan.query.filter(
					RecipePlan.user_id == user_id,
					func.date(RecipePlan.date) == today
				).all()
		
		if today_plan:
			today_recipe_ids = [plan.recipe_id for plan in today_plan]
			today_recipes = Recipe.query.filter(Recipe.id.in_(today_recipe_ids)).all()
			current_app.logger.info(f"Today's recipe plan for {user_id}: {today_recipes}")
			return {
				"message": "Recipe plan for today already exists",
				"recipes": [recipe.to_dict() for recipe in today_recipes]
			}, 200

		# # Retrieve all the available recipes
		available_recipes = Recipe.query.filter(Recipe.id.notin_(recent_recipe_ids)).all()
		
		
		if not available_recipes:
			current_app.logger.info(f'No new recipe is available for user {user_id}')
			raise AppException('No new recipes available to create a plan', 400)

		# # Randomly select recipes for the day
		selected_recipes = random.sample(available_recipes, min(2, len(available_recipes)))

		# # Save the plan for the day
		today = datetime.now()
		for recipe in selected_recipes:
			recipe_plan = RecipePlan(
				user_id=user_id,
				recipe_id=recipe.id, 
				date=today
			)
			db.session.add(recipe_plan)
		
		db.session.commit()
		current_app.logger.info(f'Created new recipe plan for user {user_id} successfully')
		return {"message": "New daily recipe plan created", "recipes": [recipe.to_dict() for recipe in selected_recipes]}, 200
					 