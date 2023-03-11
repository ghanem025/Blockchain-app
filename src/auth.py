from flask import Blueprint, render_template, redirect, url_for, flash, request, send_file
from io import BytesIO
import zipfile

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

auth = Blueprint('auth', __name__)

@auth.route('/generate_key')
def key_page():
    return  render_template('generate.html')

# Generating public and private keys
@auth.route('/generate_key', methods=['POST'])
def generate_key():
    private_key = rsa.generate_private_key(public_exponent = 65537, key_size = 4096, backend=default_backend())

    encrypted_private_key = private_key.private_bytes(encoding = serialization.Encoding.PEM, 
                                                   format = serialization.PrivateFormat.PKCS8, 
                                                   encryption_algorithm = 
                                                   serialization.NoEncryption())                                  
    public_key = private_key.public_key()
    public_key_pem = public_key.public_bytes(encoding = serialization.Encoding.PEM, format = serialization.PublicFormat.SubjectPublicKeyInfo)

    zip_obj = BytesIO()
    with zipfile.ZipFile(zip_obj, mode='w') as zip_file:
        zip_file.writestr('private_key.pem', encrypted_private_key)
        zip_file.writestr('public_key.pem', public_key_pem)
    zip_obj.seek(0)

    return send_file(zip_obj, as_attachment=True, download_name = "keys.zip")
