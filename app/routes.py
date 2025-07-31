from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, current_user  # ✅ ADD THIS
from app import db
from app.models import User

main = Blueprint('main', __name__)

chat_rooms = []  # simple in-memory list

@main.route('/chat/<room_id>')
def chat(room_id):
    if room_id not in chat_rooms:
        flash("Room doesn't exist.")
        return redirect(url_for('main.home'))
    return render_template('chat.html', room=room_id)

@main.route('/')
def index():
    return redirect(url_for('main.login'))

@main.route('/home')
def home():
    return render_template('home.html',rooms=chat_rooms)

@main.route('/create_room', methods=['POST'])
def create_room():
    room_id = f"room{len(chat_rooms)+1}"
    chat_rooms.append(room_id)
    return redirect(url_for('main.home'))

@main.route('/delete_room/<room_id>', methods=['POST'])
def delete_room(room_id):
    if room_id in chat_rooms:
        chat_rooms.remove(room_id)
    return redirect(url_for('main.home'))

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
