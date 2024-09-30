from .extensions import db
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash
from .utils import safe_json_load, serializeJsonToString


# ===================
# User Entity Class
# ===================
class User(db.Model):
	# # User attributes
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	username = db.Column(db.String(80), unique=True, nullable=False)
	password_hash = db.Column(db.String(150), nullable=False)
	role = db.Column(db.String(50), nullable=False)
	allergies = db.Column(db.Text)
	dislikes = db.Column(db.Text)
	hard_to_get = db.Column(db.Text)
	family_size = db.Column(db.Integer)
	aveg_intake_person = db.Column(db.Integer)
	created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
	updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
	# # Relationship with recipes (one-to-many)
	recipes = db.relationship('Recipe', backref='user', lazy='dynamic')
	# # Relationship with pins (one-to-many)
	pins = db.relationship('Pin', backref='user', lazy='dynamic') 	

	
	def set_password(self, password) -> None: # # Converts the password from plain text to hash string
		self.password_hash = generate_password_hash(password)
	
	def check_password(self, password) -> bool: # # Checks provided password against hashed password stored in the database
		return check_password_hash(self.password_hash, password)
	
	def to_dict(self) -> dict: # # Give a dictionary representation of the class
		return {
            "id": self.id,
            "username": self.username,
			'role': self.role,
            "allergies": serializeJsonToString(self.allergies),
			"dislikes": serializeJsonToString(self.dislikes),
			"hard_to_get": serializeJsonToString(self.hard_to_get),
            "family_size": self.family_size,
            "aveg_intake_person": self.aveg_intake_person,
			"created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": self.updated_at.strftime("%Y-%m-%d %H:%M:%S")
        }

	def __repr__(self) -> str: # # Return string representation of User class for debug
		return f'<User {self.username}>'



# ====================
# Recipe Entity Class
# ====================
class Recipe(db.Model):
	"""
	Attribute: ingredients
	ingredients -- passing methology
	{
		'item': {'quantityty': 'value', 'cost': 'value'}
	}
	"""	
	# # Recipe attributes
	__tablename__ = 'recipes'
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	name = db.Column(db.String(255), nullable=False)
	ingredients =db.Column(db.Text, nullable=False)
	instructions = db.Column(db.Text, nullable=False)
	category = db.Column(db.String(100))
	# # TODO
	# amount_to_serve = db.Column(db.Integer, nullable=False)
	total_cost_ingred = db.Column(db.Float, nullable=True) # # Auto calculated
	created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
	created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
	updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
	# # Relationships with pin
	pins = db.relationship('Pin', backref='recipe', cascade="all, delete-orphan", lazy='dynamic')


	def calculate_total_cost(self, ingredients): # # Setter method for ingredients
		"""
		Dynamically set the total cost of ingredients.
		Expect ingredients in JSON format:
		{
			'item_name': {'quantity': numeric_value, 'cost': numeric_value}
		}
		"""
		ingredients = safe_json_load(ingredients)
		total_cost = 0
		
		for item in ingredients.values():
			try:
				cost = float(item.get('cost', 0))
				qty = float(item.get('quantity', 0))
				total_cost += cost * qty
			except (TypeError, ValueError):
				continue # # Skip invalid entries

		self.total_cost_ingred = float(total_cost)


	def to_dict(self) -> dict: # # Give a dictionary representation of the class
		return {
            "id": self.id,
            "name": self.name,
            "ingredients": safe_json_load(self.ingredients),
            "instructions": serializeJsonToString(self.instructions),
            "category": self.category,
            # "amount_to_serve": self.amount_to_serve,
            "total_cost_ingred": self.total_cost_ingred,
            "created_by": self.created_by,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }
	

	def __repr__(self) -> str: # # Class String representation for debug
		return f'<Recipe {self.name} - {self.category}>'
	


# ===========================
# Comment-(Pin) Entity Class
# ===========================
class Pin(db.Model):
	# # Pin class attributes
	__tablename__ = 'pins'
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
	content = db.Column(db.Text, nullable=False)
	created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
	updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


	def to_dict(self) -> dict: # # Give a dictionary representation of the class
		return {
            "id": self.id,
            "recipe_id": self.recipe_id,
            "user_id": self.user_id,
            "content": serializeJsonToString(self.content),
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
			"updated_at": self.updated_at.strftime("%Y-%m-%d %H:%M:%S")
        }
	
	def __repr__(self) -> str: # # Pin class string representation
		return f'<Pin {self.id} -- {self.content}>'



# =============================
# Blacklist Token Entity Class
# =============================
class BlacklistToken(db.Model):
	__tablename__ = 'blacklist_tokens'
	id = db.Column(db.Integer, primary_key=True)
	token = db.Column(db.String(500), nullable=False)
	blacklisted_on = db.Column(db.DateTime(timezone=True), default=db.func.now())
	
	def __repr__(self): # # String representation
		return f'<BlacklistToken {self.token}>'



# ======================
# Recipe plan Entity
# ======================
class RecipePlan(db.Model):
	__tablename__ = 'recipe_plans'
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
	data = db.Column(db.DateTime(timezone=True), default=func.now())
	
