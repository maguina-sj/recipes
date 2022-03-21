from flask_app import app
from flask import Flask, render_template, redirect, session, request, flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask_app.models.recipe import Recipe
from flask_app.models.user import User

@app.route('/recipes/new')
def newRecipe():
    if 'user_id' not in session:
        flash("You must be logged in to view this page")
        return redirect('/')
    return render_template('create.html')

@app.route('/recipes/create', methods=['POST'])
def createRecipe():
    if 'user_id' not in session:
        flash("You must be logged in to view this page")
        return redirect('/')
    if not Recipe.validate_recipe(request.form):
        return redirect('recipes/new')
    data = {
        'name' : request.form['name'],
        'description' : request.form['description'],
        'instructions' : request.form['instructions'],
        'thirtymin' : int(request.form['thirtymin']),
        'date_made' : request.form['date_made'],
        'user_id' : session['user_id']
        
    }
    Recipe.save(data)
    print('recipe was saved')
    return redirect('/dashboard')

@app.route('/recipes/edit/<int:id>')
def editRecipe(id):
    data = {
        'id' : id
    }
    user_data = {
        'id' : session['user_id']
    }
    return render_template('edit.html', recipe=Recipe.getOne(data), user= User.getOne(user_data))

@app.route('/recipes/update/<int:id>', methods=['POST'])
def updateRecipe():
    if 'user_id' not in session:
        flash("You must be logged in to view this page")
        return redirect('/')
    if not Recipe.validate_recipe(request.form):
        return redirect('recipes/new')
    data = {
        'name' : request.form['name'],
        'description' : request.form['description'],
        'instructions' : request.form['instructions'],
        'thirtymin' : int(request.form['thirtymin']),
        'date_made' : request.form['date_made'],
        'id' : request.form['id']
    }
    Recipe.update(data)
    return redirect('/dashboard')

@app.route('/recipes/show/<int:id>')
def showRecipe(id):
    if 'user_id' not in session:
        flash("You must be logged in to view this page")
        return redirect('/')
    data = {
        'id' : id
    }
    user_data = {
        'id' : session['user_id']
    }
    return render_template('show.html', recipe = Recipe.getOne(data), user=User.getOne(user_data))

@app.route('/recipes/delete/<int:id>')
def deleteRecipe(id):
    if 'user_id' not in session:
        flash("You must be logged in to view this page")
        return redirect('/')
    data = {
        'id' : id
    }
    Recipe.delete(data)
    return redirect('/dashboard')