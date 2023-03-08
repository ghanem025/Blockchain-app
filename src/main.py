# Python program to create Blockchain
import json
import zlib
from flask import Blueprint
from flask import Flask, jsonify, render_template, request, send_file
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

@main.route('/update_key', methods=['POST'])
def update_file():
    from io import BytesIO

    public_key = request.form.get('publickey')
    public_key_file = BytesIO(bytes(public_key, "utf-8"))
    return send_file(public_key_file, download_name = "public_key.pem")

@main.route('/adding_block', methods=['POST'])
def add_block():
    import uuid
    uuidOne = uuid.uuid1() 
    public_key_data = request.form.get('publickey')    
    public_key = serialization.load_pem_public_key(public_key_data.encode())
    public_key_data = public_key_data + str(uuidOne) + '\n'
    diagnosis = request.form.get('diagnosis')
    doctor = request.form.get('doctor')
    symptoms = request.form.get('symptoms')
    treatment = request.form.get('treatment')
    prescription = request.form.get('prescription')

    diagnosis = zlib.compress(bytes(diagnosis, 'utf-8'), level=9)
    doctor = zlib.compress(bytes(doctor, 'utf-8'), level=1)
    symptoms = zlib.compress(bytes(symptoms, 'utf-8'), level=9)
    treatment = zlib.compress(bytes(treatment, 'utf-8'), level=9)
    prescription = zlib.compress(bytes(prescription, 'utf-8'), level=1)

    diagnosis = base64.b64encode(public_key.encrypt(
		diagnosis,
		padding.OAEP(
			mgf=padding.MGF1(algorithm=hashes.SHA256()),
			algorithm=hashes.SHA256(),
			label=None
		)
	)).decode('utf-8')
    doctor = base64.b64encode(public_key.encrypt(
		doctor,
		padding.OAEP(
			mgf=padding.MGF1(algorithm=hashes.SHA256()),
			algorithm=hashes.SHA256(),
			label=None
		)
	)).decode('utf-8')
    symptoms = base64.b64encode(public_key.encrypt(
		symptoms,
		padding.OAEP(
			mgf=padding.MGF1(algorithm=hashes.SHA256()),
			algorithm=hashes.SHA256(),
			label=None
		)
	)).decode('utf-8')
    treatment = base64.b64encode(public_key.encrypt(
		treatment,
		padding.OAEP(
			mgf=padding.MGF1(algorithm=hashes.SHA256()),
			algorithm=hashes.SHA256(),
			label=None
		)
	)).decode('utf-8')
    prescription = base64.b64encode(public_key.encrypt(
		prescription,
		padding.OAEP(
			mgf=padding.MGF1(algorithm=hashes.SHA256()),
			algorithm=hashes.SHA256(),
			label=None
		)
	)).decode('utf-8')
    
    blockchain.add_new_transaction(1)
    print(blockchain.mine(str(uuidOne), diagnosis, doctor, symptoms, treatment, prescription))
    return render_template("update_key.html", key=public_key_data)

@main.route('/upload', methods=['POST'])
def upload_key():
	uploaded_file = request.files['file']
	file_info = uploaded_file.read().decode('utf-8').replace("\\n", "\n")
	return render_template('add_block.html', key=file_info)
