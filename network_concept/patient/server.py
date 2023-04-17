import socket
import pickle
from blockchain import Blockchain

HOST = '0.0.0.0'
PORT = 5000 
print("Socket started")

def encrypt_data(temp_dict, public_key_data):
    try:
        public_key = serialization.load_pem_public_key(public_key_data)
    except ValueError as e:
        print("There was an error reading the public key, make sure to upload a public key before adding a block")
        return temp_dict
    fields = ['diagnosis', 'doctor', 'symptoms', 'treatment', 'prescription']
    for values in fields:
        temp_dict[values] = base64.b64encode(public_key.encrypt(
            temp_dict[values].encode(),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )).decode('utf-8')
    return temp_dict

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(8138)
            if not data:
                print("there is no data")
                break
            # Process the received data here
            loaded_data = pickle.loads(data)
            public_key_data, signature, message, block = loaded_data
            print("we got the data")
            print(public_key_data)
            b = Blockchain()
            contract = b.SmartContract()
            if not contract.check_signature(public_key_data, signature, message):
                print("WARNING DOCTOR IS NOT VERIFIED TO MAKE REQUEST")
                conn.sendall(b'You are not allowed to access this data')
    
            block = pickle.loads(block)
            temp_dict = dict(block.__dict__)
            fields = ['diagnosis', 'doctor', 'symptoms', 'treatment', 'prescription']
            with open('private_key.pem', 'r') as f:
                private_key_data = f.read()
            try:
                from cryptography.hazmat.primitives import serialization
                
                private_key = serialization.load_pem_private_key(private_key_data.encode(), password=None)
            except ValueError:
                print("cannot read file it is not .pem format")
            import base64
            from cryptography.hazmat.primitives.asymmetric import padding
            from cryptography.hazmat.primitives import hashes
            for field in fields:
                temp_dict[field] = private_key.decrypt(
                    base64.b64decode(temp_dict[field]),
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None
                    )
                ).decode('utf-8')
            print(temp_dict)
            temp_dict = encrypt_data(temp_dict, public_key_data)
            print(temp_dict)
            import json
            json_string = json.dumps(temp_dict)
            conn.sendall(json_string.encode())



