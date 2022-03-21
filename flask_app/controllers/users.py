from flask_app import app
from flask import Flask, render_template, redirect, session, request, flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask_app.models.user import User
from flask_app.models.recipe import Recipe

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def registerUser():
    is_valid = User.validate_user(request.form)
    if not is_valid:
        return redirect ('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    data = {
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'email' : request.form['email'],
        'password' : pw_hash
    }
    id = User.save(data)
    if not id: 
        flash("Uh Oh! What happened?!")
        return redirect('/')
    session['user_id'] = id
    flash("Great! You're logged in!")
    return redirect('/dashboard')

@app.route('/login', methods=['POST'])
def login():
    user = User.getByEmail(request.form)
    print(user)
    if not user:
        flash("This email is not in the database, please register")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Wrong Password")
        return redirect('/')
    session['user_id'] = user.id
    flash('You are now logged in')
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash("You must be logged in to view this page")
        return redirect('/')
    data = {
        'id' : session['user_id']
    }
    return render_template('dashboard.html', user=User.getOne(data), recipes=Recipe.getAll())

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')