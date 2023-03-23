from hashlib import sha256
import json
import os
import pickle
import requests
import socket
import sys
import time
import uuid
import zlib

#This is my own implementation of a blockchain.
class Block:
    # keep the previous hash in a block to semi-protect the chains integrity
    # we use a nonce value, a nonce value is a value or a number that can only be used once
    def __init__(self, uuidOne, diagnosis, doctor, symptoms, treatment, prescription, index, transaction, timestamp, previous_hash, nonce = 0):
        self.uuidOne = uuidOne
        self.diagnosis = diagnosis
        self.doctor = doctor
        self.symptoms = symptoms
        self.treatment = treatment
        self.prescription = prescription
        self.index = index
        self.transaction = transaction
        self.timestamp = timestamp
        self.previous_hash = previous_hash

    def create_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return sha256(block_string.encode()).hexdigest()
    
class Blockchain:
    def __init__(self):
        self.unconfirmed_transactions = [] #maybe we can have the doctor's transaction stored here?
        self.chain = []
        self.block_is_valid = None
        self.load_chain()
        self.host = self.get_host()
        self.port = 5000
        self.nodes = {} # list of all the nodes on the network
        # self.contract = self.SmartContract()

    # class SmartContract:

    #     def check_signature(self, key, signature, message):
    #         # check the auth_doctor dict and see if they are there
    #         # if they are not the contract will refuse the transaction.
    #         # otherwise we continue s\
    #         from cryptography.hazmat.primitives.asymmetric import padding, rsa
    #         from cryptography.hazmat.primitives import serialization, hashes
    #         from cryptography.exceptions import InvalidSignature
    #         public_key = serialization.load_pem_public_key(key.encode())
    #         if key.strip():
    #             try:
    #                 public_key.verify(
    #                     signature,
    #                     message,
    #                     padding.PSS(
    #                         mgf=padding.MGF1(hashes.SHA256()),
    #                         salt_length=padding.PSS.MAX_LENGTH
    #                     ),
    #                     hashes.SHA256()
    #                 )
    #                 print('Signature is valid')
    #             except InvalidSignature:
    #                 print('Signature is invalid')
    #             # self.send_request()
    #             return True
    #         else:
    #             print("request not allowed")
    #             return False
    
    def wait_for_request(self):
        HOST = '0.0.0.0'
        PORT = 5000 
        print("Socket started")
           
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen()
            conn, addr = s.accept()
            with conn:
                print('Connected by', addr)
                while True:
                    data = conn.recv(4096)
                    if not data:
                        break
                    # Process the received data here
                    data_variable = pickle.loads(data)
                    print(
                        f'''
                        Diagnosis:{data_variable.diagnosis}
                        Doctor: {data_variable.doctor}
                        symptoms: {data_variable.symptoms}
                        treatment: {data_variable.treatment}
                        prescription: {data_variable.prescription}
                        ''')

    def wait_for_block(self):
        HOST = '0.0.0.0'
        PORT = 5000 
        print("Socket started")
           
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen()
            conn, addr = s.accept()
            with conn:
                print('Connected by', addr)
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    # Process the received data here
                    data_variable = data
                    print(data)

    def send_request(self, transaction_id):
        HOST = '127.0.0.1'  # The server's hostname or IP address
        PORT = 5000       # The port used by the server
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
                                # decrypt_data(data_variable)
            print(f'id is {transaction_id}')
            fields = ['diagnosis', 'doctor', 'symptoms', 'treatment', 'prescription']
            for block in self.chain:
                print(f"found block {block.doctor}")
                temp_dict = dict(block.__dict__)
                if temp_dict['uuidOne'] in transaction_id: # come back for performance optimization
                    print("SENDING BLOCK")
                    s.sendall(pickle.dumps(block))
            data = s.recv(4096)
            print('Received:', data)

    def send_block(self,first_block):
        HOST = '127.0.0.1'  # The server's hostname or IP address
        PORT = 5000       # The port used by the server
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.sendall(pickle.dumps(first_block))
            data = s.recv(1024)
            print('Received:', data)


    def add_node(self, host, port):
        node = {"host": host, "port": port}
        self.nodes[host + ":" + str(port)] = node

    def remove_node(self, host, port):
        del self.nodes[host + ":" + str(port)]

    def get_nodes(self):
        return list(self.nodes.values())

    def get_host(self):

        # fetch public IP address from ifconfig.co
        url = 'https://ifconfig.co/ip?4'
        response = requests.get(url)
        public_ip = response.text.strip()

        return public_ip
        
    def create_genesis_block(self):
        uuidOne = uuid.uuid1()
        first_block = Block(str(uuidOne) ,"flu", "Dr.Balls", "itchy ball", "amputation", "crack", 0, [], time.strftime('%X %x %Z'), "0") # I used time.strftime for an acurate date
        first_block.hash = first_block.create_hash()
        self.chain.append(first_block)
        self.save_chain()
    
    @property
    def last_block(self):
        return self.chain[-1]
    
    @property
    def get_status(self):
        return self.block_is_valid

    def save_chain(self):
        with open('blockchain.pickle', 'wb') as f:
            pickle.dump(self.chain, f)
            print("Blockchain has been saved")
            
    def load_chain(self):
        try:
            with open('blockchain.pickle', 'rb') as f:
                self.chain = pickle.load(f)
                print("Blockchain has been loaded")
        except FileNotFoundError:
            print("blockchain does not exist")
            self.create_genesis_block()

    difficulty = 2
    def proof_of_work(self, block):
        block.nonce = 0
        finished_hash = block.create_hash()
        while not finished_hash.startswith('0' * Blockchain.difficulty):
            block.nonce += 1
            finished_hash = block.create_hash()
        return finished_hash
    
    def add_block(self, block, proof):
        previous_hash = self.last_block.hash
        # comparing the chains last block and the block objects previous hash
        if previous_hash != block.previous_hash:
            print("ERROR: Something went wrong, the blockchains previous hash does not match the previous_hash of the block, block will not be added to chain")
            return False
        if not self.is_valid_proof(block, proof):
            self.block_is_valid = False
            return False

        block.hash = proof
        self.chain.append(block)
        self.save_chain()
        return True
    
    def is_valid_proof(self, block, block_hash):
        self.block_is_valid = True
        return (block_hash.startswith('0' * Blockchain.difficulty) and block_hash == block.create_hash())
    
    def add_new_transaction(self, block):
        self.unconfirmed_transactions.append(block.transaction)# the current transaction will be stored here
        return self.mine(block)

    def mine(self, new_block):
        import time
        if not self.unconfirmed_transactions:
            return False
        print("MINE")
        proof = self.proof_of_work(new_block)
        self.add_block(new_block, proof)
        self.unconfirmed_transactions = []
        return new_block.index
    
    def create():
        b = Blockchain()
        return b
