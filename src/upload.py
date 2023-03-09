from flask import Blueprint
from flask import Flask, jsonify, render_template, request


upload = Blueprint('upload', __name__)

@upload.route('/upload_keys')
def upload_key_site():
	return render_template('upload_key.html')

# upload public key for add block page
@upload.route('/upload', methods=['POST'])
def upload_key():
    uploaded_file = request.files['public_file']
    file_info = uploaded_file.read().decode('utf-8').replace("\\n", "\n")
    return render_template("add_block.html", public_key=file_info)

# allow user to send there private key, keys are stored on the client side
@upload.route('/upload_private', methods=['POST'])
def upload_private_key():
    uploaded_file = request.files['private_file']
    private_key = uploaded_file.read().decode('utf-8').replace("\\n", "\n")
    return render_template('upload_key.html', private_key = private_key)

# allow user to send there public key, keys are stored on the client side
@upload.route('/upload_public', methods=['POST'])
def upload_public_key():
    uploaded_file = request.files['public_file']
    public_key = uploaded_file.read().decode('utf-8').replace("\\n", "\n")

    return render_template('upload_key.html', public_key = public_key)
