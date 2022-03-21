from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Recipe:
    db = 'recipes'
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.thirtymin = data['thirtymin']
        self.date_made = data['date_made']

    @staticmethod
    def validate_recipe(recipe):
        is_valid = True
        if len(recipe['name']) < 3:
            flash("Name must be at least 3 character.")
            is_valid = False
        if len(recipe['description']) < 3:
            flash("Description must at least 3 characters.")
            is_valid = False
        if len(recipe['instructions']) < 3:
            flash("Instructions must be at least 3 characters.")
            is_valid= False
        return is_valid

    @classmethod
    def save(cls,data):
        query = 'INSERT INTO recipes (name, description, instructions, user_id, thirtymin, date_made) VALUES (%(name)s, %(description)s, %(instructions)s, %(user_id)s, %(thirtymin)s, %(date_made)s);'
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def update(cls, data):
        query = 'UPDATE recipes SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, thirtymin = %(thirtymin)s, date_made = %(date_made)s,  WHERE id = %(id)s;'
        return connectToMySQL(cls.db).query_db(query, data)


    @classmethod
    def delete(cls, data):
        query = 'DELETE FROM recipes WHERE id = %(id)s;'
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def getOne(cls, data):
        query = 'SELECT * FROM recipes WHERE id = %(id)s;'
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def getAll(cls):
        query = 'SELECT * FROM recipes;'
        results= connectToMySQL(cls.db).query_db(query)
        recipes = []
        for row in results:
            recipes.append(cls(row))
        return recipes
