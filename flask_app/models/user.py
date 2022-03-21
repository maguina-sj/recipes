from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.recipe import Recipe
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    db = 'recipes'
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.recipes = []

    @staticmethod
    def validate_user(user):
        is_valid = True
        if len(user['first_name']) < 2:
            flash("Name must be at least 2 character.")
            is_valid = False
        if len(user['last_name']) < 2:
            flash("Last Name must at least 2 characters.")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!")
            is_valid = False
        if user['password'] != user['confirm_password']:
            flash('Passwords do not match')
            is_valid = False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters.")
            is_valid= False
        return is_valid

    @classmethod
    def getOne(cls, data):
        query = 'SELECT * FROM users WHERE id = %(id)s;'
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def save(cls, data):
        query = 'INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);'
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def allRecipes(cls, data):
        query = 'SELECT * FROM users LEFT JOIN users ON user.id = recipes.user_id WHERE recipe.id = %(id)s;'
        results = connectToMySQL(cls.db).query_db(query, data)
        print("all recipes results: ", results)
        user = cls(results[0])
        for row in results:
            RecipeData = {
                'id' : row['recipes.id'],
                'name' : row['name'],
                'description' : row['description'],
                'instructions' : row['instructions'],
                'created_at' : row['recipes.created_at'],
                'updated_at' : row['recipes.updated_at']
            }
            print("each row of RecipeData from models: ", row)
            user.recipes.append(Recipe(RecipeData))
            print("print the recipe list from models: ", user.recipes)
            return user

    @classmethod
    def getByEmail(cls, data):
        query = 'SELECT * FROM users WHERE email = %(email)s;'
        result = connectToMySQL(cls.db).query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])