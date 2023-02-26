# Python program to create Blockchain
import json
from flask import Blueprint
from flask import Flask, jsonify, render_template, request
from . import db
from .blockchain import Blockchain


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

@main.route('/info')
def info():
	return render_template('info.html')

@main.route('/profile')
def profile():
	return render_template('profile.html')

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



	
	

	

