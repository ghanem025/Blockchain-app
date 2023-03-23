from flask import Blueprint, render_template, redirect, url_for, flash, request, send_file
from io import BytesIO
import zipfile

from .blockchain import Blockchain
from .blockchain import Block

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import re

auth = Blueprint('auth', __name__)

@auth.route('/send_request', methods=['POST'])
def send_request():
    public_key_data = request.form.get('publickey')
    private_key_data = request.form.get('privatekey')
    transaction_id = request.form.get('transactionID')
    try:
        transactions = public_key_data.split('-----END PUBLIC KEY-----')[0] + '-----END PUBLIC KEY-----'
        private_key = serialization.load_pem_private_key(private_key_data.encode(), password=None)
    except ValueError:
        flash("There was an error reading your private key or public, make sure you are uploading your private key not your public key", "Valerr")
        return redirect(url_for('upload.upload_key_site'))
    print(transactions)
    message = b'I am Dr. Balls I would like to view your PHR plz'
    signature = private_key.sign(
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    # b = Blockchain()
    # contract = b.SmartContract()
    # if contract.check_signature(transactions, signature, message):
    #     print("contract working")
    #     b.send_request(transaction_id)

    return render_template('send_request.html')


@auth.route('/generate_patient_key')
def patient_key_page():
    return  render_template('patient_key.html')

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
