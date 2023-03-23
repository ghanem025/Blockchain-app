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
from flask import Flask, jsonify, render_template, request, send_file, redirect, flash, url_for

# Creating the Web
# App using flask
main = Blueprint('main', __name__)

# Create the object
# of the class blockchain
blockchain = Blockchain()

#default route
@main.route('/doctor')
def doctor_site():
    return render_template('doctor.html')

 
@main.route('/patient')
def patient_site():
    return render_template('patient.html')

#default route
@main.route('/')
def index():
    return render_template('index.html')

@main.route('/doctor_wiki')
def doctor_wiki_site():
    return render_template('doctor_wiki.html')

@main.route('/patient_wiki')
def patient_wiki_site():
    return render_template('patient_wiki.html')

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
    
    transaction = {
        'sender': doctor,
        'recipient': str(uuidOne)
    }
    import time
    new_block = Block(str(uuidOne), diagnosis, doctor, symptoms, treatment, 
                      prescription, blockchain.last_block.index + 1, 
                      transaction, time.strftime('%X %x %Z'), blockchain.last_block.hash)
    added_block = blockchain.add_new_transaction(new_block) 
    if not added_block:
        print("did not add block")
    return render_template("update_key.html", key=public_key_data)

# displaying block information
@main.route('/fancy_display')
def fancy_display():
    chain_data = []
    for block in blockchain.chain:
        chain_data.append(block.__dict__)
    return render_template('fancy_display.html', chain_data=chain_data)

# displaying block information
@main.route('/patient_display')
def patient_display():
    chain_data = []
    for block in blockchain.chain:
        chain_data.append(block.__dict__)
    return render_template('patient_table.html', chain_data=chain_data)


# display history
@main.route('/view_history', methods=['POST'])
def view_history():
    public_key_data = request.form.get('publickey')
    private_key_data = request.form.get('privatekey')
    transaction_id = request.form.get('transactionID')
    try:
        transactions = public_key_data.split("\r\n")[public_key_data.split('\r\n').index('-----END PUBLIC KEY-----')+1:]
        private_key = serialization.load_pem_private_key(private_key_data.encode(), password=None)
    except ValueError:
        flash("There was an error reading your private key or public, make sure you are uploading your private key not your public key", "Valerr")
        return redirect(url_for('upload.upload_key_site'))
    if transaction_id:
        transactions = transaction_id
        print("the ratnt")
    chain_data = []
    fields = ['diagnosis', 'doctor', 'symptoms', 'treatment', 'prescription']
    for block in blockchain.chain:
        temp_dict = dict(block.__dict__)
        if temp_dict['uuidOne'] in transactions: # come back for performance optimization
            for field in fields:
                try:
                    temp_dict[field] = private_key.decrypt(
                        base64.b64decode(temp_dict[field]),
                        padding.OAEP(
                            mgf=padding.MGF1(algorithm=hashes.SHA256()),
                            algorithm=hashes.SHA256(),
                            label=None
                        )
                    ).decode('utf-8')
                except ValueError:
                    flash("Could not user your private key to decrypt the data, make sure you uploaded the correct private key", "Valerr")
                    return redirect(url_for('upload.upload_key_site'))

            chain_data.append(temp_dict)
    return render_template('view_history.html', chain_data=chain_data)

