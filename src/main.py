# Python program to create Blockchain
import base64
import json
import zlib

from .blockchain import Blockchain
from .blockchain import Block
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from flask import Blueprint
from flask import Flask, jsonify, render_template, request, send_file

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

@main.route('/wiki')
def wiki_site():
    return render_template('wiki.html')

# Display blockchain in json format
@main.route('/get_chain', methods=['GET'])
def display_chain():
    chain_data = []
    for block in blockchain.chain:
        chain_data.append(block.__dict__)
    json_str = json.dumps({'length': len(chain_data),
                            'chain': chain_data})
    response = json.loads(json_str)
    
    return response

@main.route('/adding_block')
def add_block_site():
    return render_template('add_block.html')

# add UUID to public key
@main.route('/update_key', methods=['POST'])
def update_file():
    from io import BytesIO
    public_key = request.form.get('publickey')
    public_key_file = BytesIO(bytes(public_key, "utf-8"))
    return send_file(public_key_file, as_attachment=True, download_name = "public_key.pem")

# encrypt data and send data to mine a new block 
@main.route('/adding_block', methods=['POST'])
def add_block():
    import uuid
    uuidOne = uuid.uuid4() 
    public_key_data = request.form.get('publickey')
    try:
        public_key = serialization.load_pem_public_key(public_key_data.encode())
        public_key_data = public_key_data + str(uuidOne) + '\n'
    except ValueError():
        print("There was an error reading the public key, make sure to upload a public key before adding a block")
    diagnosis = request.form.get('diagnosis')
    doctor = request.form.get('doctor')
    symptoms = request.form.get('symptoms')
    treatment = request.form.get('treatment')
    prescription = request.form.get('prescription')

    diagnosis = base64.b64encode(public_key.encrypt(
		diagnosis.encode(),
		padding.OAEP(
			mgf=padding.MGF1(algorithm=hashes.SHA256()),
			algorithm=hashes.SHA256(),
			label=None
		)
	)).decode('utf-8')
    doctor = base64.b64encode(public_key.encrypt(
		doctor.encode(),
		padding.OAEP(
			mgf=padding.MGF1(algorithm=hashes.SHA256()),
			algorithm=hashes.SHA256(),
			label=None
		)
	)).decode('utf-8')
    symptoms = base64.b64encode(public_key.encrypt(
		symptoms.encode(),
		padding.OAEP(
			mgf=padding.MGF1(algorithm=hashes.SHA256()),
			algorithm=hashes.SHA256(),
			label=None
		)
	)).decode('utf-8')
    treatment = base64.b64encode(public_key.encrypt(
		treatment.encode(),
		padding.OAEP(
			mgf=padding.MGF1(algorithm=hashes.SHA256()),
			algorithm=hashes.SHA256(),
			label=None
		)
	)).decode('utf-8')
    prescription = base64.b64encode(public_key.encrypt(
		prescription.encode(),
		padding.OAEP(
			mgf=padding.MGF1(algorithm=hashes.SHA256()),
			algorithm=hashes.SHA256(),
			label=None
		)
	)).decode('utf-8')
    
    blockchain.add_new_transaction(1)
    print(blockchain.mine(str(uuidOne), diagnosis, doctor, symptoms, treatment, prescription))
    return render_template("update_key.html", key=public_key_data)

# displaying block information
@main.route('/fancy_display')
def fancy_display():
    chain_data = []
    for block in blockchain.chain:
        chain_data.append(block.__dict__)
    return render_template('fancy_display.html', chain_data=chain_data)


# display history
@main.route('/view_history', methods=['POST'])
def view_history():
    public_key_data = request.form.get('publickey')
    private_key_data = request.form.get('privatekey')
    transactions = public_key_data.split("\r\n")[public_key_data.split('\r\n').index('-----END PUBLIC KEY-----')+1:]
    print(transactions)
    private_key = serialization.load_pem_private_key(private_key_data.encode(), password=None)
    chain_data = []
    fields = ['diagnosis', 'doctor', 'symptoms', 'treatment', 'prescription']
    for block in blockchain.chain:
        temp_dict = dict(block.__dict__)
        if temp_dict['uuidOne'] in transactions: # come back for performance optimization
            for field in fields:
                temp_dict[field] = private_key.decrypt(
                    base64.b64decode(temp_dict[field]),
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None
                    )
                ).decode('utf-8')
            chain_data.append(temp_dict)
    return render_template('view_history.html', chain_data=chain_data)

