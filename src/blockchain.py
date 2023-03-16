from hashlib import sha256
import json
import os
import pickle
import sys
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
        self.create_genesis_block() # creating our first block (genesis block)
        self.block_is_valid = None
        self.load_chain()
    
    def create_genesis_block(self):
        import time
        import uuid
        uuidOne = uuid.uuid1()
        first_block = Block(str(uuidOne) ,"flu", "Dr.Balls", "itchy ball", "amputation", "crack", 0, [], time.strftime('%X %x %Z'), "0") # I used time.strftime for an acurate date
        first_block.hash = first_block.create_hash()
        self.chain.append(first_block)
    
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
            print("something is not right, the previous hash doesn't match")
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
    
    def add_new_transaction(self, transaction):
        self.unconfirmed_transactions.append(transaction)

    def mine(self, uuidOne,  diagnosis, doctor, symptoms, treatment, prescription):
        import time
        if not self.unconfirmed_transactions:
            return False
        last_block = self.last_block

        new_block = Block(uuidOne, diagnosis, 
        doctor, symptoms, treatment, prescription, index=last_block.index + 1, 
        transaction=self.unconfirmed_transactions, 
        timestamp=time.strftime('%X %x %Z'),
        previous_hash=last_block.hash)

        proof = self.proof_of_work(new_block)
        self.add_block(new_block, proof)
        self.unconfirmed_transactions = []
        return new_block.index
