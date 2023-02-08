from flask import Blueprint
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return 'login.html'

@auth.route('/signup')
def signup():
    return 'signup.html'

@auth.route('/logout')
def logout():
    return 'logout'