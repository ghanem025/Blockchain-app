from flask import Blueprint, render_template, redirect, url_for, flash, request
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

auth = Blueprint('auth', __name__)


# @auth.route('/generate_key')
# def generate_key():
#     return  render_template('generate.html')


def save_file(filename, content):
	f = open(filename, "wb")
	f.write(content)
	f.close()

@auth.route('/generate_key')
def key_page():
    return  render_template('generate.html')


# Generating private keys
@auth.route('/generate_key', methods=['POST'])
def generate_key():
    private_key = rsa.generate_private_key(public_exponent = 65537, key_size = 4096, backend=default_backend())

    private_key_pass = request.form.get('password')

    password = generate_password_hash(private_key_pass, method='sha256')

    password_byte = bytes(password, 'utf-8')

    encrypted_private_key = private_key.private_bytes(encoding = serialization.Encoding.PEM, 
                                                   format = serialization.PrivateFormat.PKCS8, 
                                                   encryption_algorithm = 
                                                   serialization.BestAvailableEncryption(password_byte))
    save_file("private_key.pem", encrypted_private_key)

    public_key = private_key.public_key()
    public_key_pem = public_key.public_bytes(encoding = serialization.Encoding.PEM, format = serialization.PublicFormat.SubjectPublicKeyInfo)

    save_file("public_key.pem", public_key_pem)

    return "keys have been created"



@auth.route('/login')
def login():
    return  render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():

    # login code goes here
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))

    return redirect(url_for('main.profile'))

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    user = User.query.filter_by(email=email).first()

    if user:
        flash("Email address already exists")
        return redirect(url_for('auth.signup'))
    
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))
    
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))

@auth.route('/logout')
def logout():
    return 'logout'
    
