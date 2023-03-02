# Python program to create Blockchain
import json
import zlib
from flask import Blueprint
from flask import Flask, jsonify, render_template, request
from .blockchain import Blockchain
from .blockchain import Block
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
import base64

# Creating the Web
# App using flask
main = Blueprint('main', __name__)

# Create the object
# of the class blockchain
blockchain = Blockchain()

#default route
@main.route('/')
def index():
    return render_template('index.html')

# Display blockchain in json format
@main.route('/get_chain', methods=['GET'])
def display_chain():
    chain_data = []
    for block in blockchain.chain:
        chain_data.append(block.__dict__)
        print("A BLOCK")
    json_str = json.dumps({'length': len(chain_data),
                            'chain': chain_data})
    response = json.loads(json_str)
    
    return response

@main.route('/adding_block')
def add_block_site():
    return render_template('add_block.html')

@main.route('/adding_block', methods=['POST'])
def add_block():
    public_key = request.form.get('publickey').replace("\\n", "\n")
    public_key = serialization.load_pem_public_key(public_key.encode())

    diagnosis = base64.b64encode(public_key.encrypt(
		request.form.get('diagnosis').encode(),
		padding.OAEP(
			mgf=padding.MGF1(algorithm=hashes.SHA256()),
			algorithm=hashes.SHA256(),
			label=None
		)
	)).decode('utf-8')
    doctor = base64.b64encode(public_key.encrypt(
		request.form.get('doctor').encode(),
		padding.OAEP(
			mgf=padding.MGF1(algorithm=hashes.SHA256()),
			algorithm=hashes.SHA256(),
			label=None
		)
	)).decode('utf-8')
    symptoms = base64.b64encode(public_key.encrypt(
		request.form.get('symptoms').encode(),
		padding.OAEP(
			mgf=padding.MGF1(algorithm=hashes.SHA256()),
			algorithm=hashes.SHA256(),
			label=None
		)
	)).decode('utf-8')
    treatment = base64.b64encode(public_key.encrypt(
		request.form.get('treatment').encode(),
		padding.OAEP(
			mgf=padding.MGF1(algorithm=hashes.SHA256()),
			algorithm=hashes.SHA256(),
			label=None
		)
	)).decode('utf-8')
    prescription = base64.b64encode(public_key.encrypt(
		request.form.get('prescription').encode(),
		padding.OAEP(
			mgf=padding.MGF1(algorithm=hashes.SHA256()),
			algorithm=hashes.SHA256(),
			label=None
		)
	)).decode('utf-8')
    
    blockchain.add_new_transaction(1)
    print(blockchain.mine(diagnosis, doctor, symptoms, treatment, prescription))
    return render_template('add_block.html')