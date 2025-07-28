from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, current_user  # ✅ ADD THIS
from app import db
from app.models import User

main = Blueprint('main', __name__)

@main.route('/chat')
def chat():
    if current_user.is_authenticated:
        return render_template('chat.html')  # ✅ Pass username to template
    else:
        flash('You must be logged in to access the chat.')
        return redirect(url_for('main.login'))

@main.route('/')
def index():
    return redirect(url_for('main.login'))

@main.route('/home')
def home():
    return render_template('home.html')
    
@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please login.')
            return redirect(url_for('main.login'))

        hashed_pw = generate_password_hash(password)
        new_user = User(username=username, password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful. Please login.')
        return redirect(url_for('main.login'))

    return render_template('register.html')


@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)  # ✅ Log the user in properly
            flash('Login successful.')
            return redirect(url_for('main.home'))
        else:
            flash('Invalid username or password.')

    return render_template('login.html')
