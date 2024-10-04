from flask import Blueprint
from flask_restful import Api
from .app_resources import GetRecipePlan, RecipeCreate, RecipeGetAll, RecipeDeleteById,RecipeUpdateById, RecipeGetById, PinCreate, PinGetByRecipeId
from .auth_resources import Signup, Login, Logout, UpdateUserProfile, DeleteUser, DeleteUserById


# ==============================================
# Instantiate and Initialize  Blueprint and Api 
# ==============================================
api_blueprint = Blueprint('api', __name__) # # Instantiate and register Blueprint for the resources
api = Api(api_blueprint) # # Instantiate and register the Blueprint with the API class


# ====================================
# Routes - Add Class Resources to API 
# ====================================
# # User
api.add_resource(Login, '/auth/login') # # POST Login
api.add_resource(Logout, '/auth/logout') # # POST Logout
api.add_resource(Signup, '/auth/users') # # POST Signup
api.add_resource(UpdateUserProfile, '/auth/users') # # PUT update user 
api.add_resource(DeleteUser, '/auth/users') # # DELETE remove user
api.add_resource(DeleteUserById, '/auth/users/<int:user_id>') # # DELETE remove user by Id

# # Recipe
api.add_resource(RecipeGetAll, '/recipes') # # GET Recipe
api.add_resource(RecipeCreate, '/recipes') # # POST Recipe
api.add_resource(RecipeGetById, '/recipes/<int:recipe_id>') # # GET Recipe by Id 
api.add_resource(RecipeDeleteById, '/recipes/<int:recipe_id>') # # DELETE Recipe by Id
api.add_resource(RecipeUpdateById, '/recipes/<int:recipe_id>') # # UPDATE Reciep by Id

# # Pin
api.add_resource(PinCreate, '/recipes/<int:recipe_id>/pin') # # POST pin/comment on a recipe identified by Id
api.add_resource(PinGetByRecipeId, '/recipes/<int:recipe_id>/pin') # # GET all pins/comments attached to a recipe

# # Recipe plan
api.add_resource(GetRecipePlan, '/daily_recommendations') # # GET 3 or less recipes for the day 