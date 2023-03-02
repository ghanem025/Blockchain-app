from hashlib import sha256
import json
import sys

#This is my own implementation of a blockchain.

print("blockchain implementation")


class Block:
    # keep the previous hash in a block to semi-protect the chains integrity
    # we use a nonce value, a nonce value is a value or a number that can only be used once
    def __init__(self, name, age, diagnosis, doctor, index, transaction, timestamp, previous_hash, nonce = 0):
        self.name = name
        self.age = age
        self.diagnosis = diagnosis
        self.doctor = doctor
        self.index = index
        self.transaction = transaction
        self.timestamp = timestamp
        self.previous_hash = previous_hash

    def create_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return sha256(block_string.encode()).hexdigest()
    
import time

class Blockchain:
    def __init__(self):
        self.unconfirmed_transactions = [] #maybe we can have the doctor's transaction stored here?
        self.chain = []
        self.create_genesis_block() # creating our first block (genesis block)
        self.block_is_valid = None

    
    def create_genesis_block(self):
        first_block = Block("patient", "30", "flu", "Dr.Balls", 0, [], time.strftime('%X %x %Z'), "0") # I used time.strftime for an acurate date
        first_block.hash = first_block.create_hash()
        self.chain.append(first_block)
    
    @property
    def last_blocK(self):
        return self.chain[-1]
    
    @property
    def get_status(self):
        return self.block_is_valid
    
    difficulty = 2
    def proof_of_work(self, block):
        block.nonce = 0
        finished_hash = block.create_hash()
        while not finished_hash.startswith('0' * Blockchain.difficulty):
            block.nonce += 1
            finished_hash = block.create_hash()
        return finished_hash
    
    def add_block(self, block, proof):
        previous_hash = self.last_blocK.hash
        # comparing the chains last block and the block objects previous hash
        if previous_hash != block.previous_hash:
            print("something is not right, the previous hash doesn't match with the blockchains previous hash", file=sys.stderr)
            return False
        if not self.is_valid_proof(block, proof):
            self.block_is_valid = False
            return False

        block.hash = proof
        self.chain.append(block)
        return True
    
    def is_valid_proof(self, block, block_hash):
        print("HI I AM TESTING VALID THING")
        self.block_is_valid = True
        return (block_hash.startswith('0' * Blockchain.difficulty) and block_hash == block.create_hash())
    
    def add_new_transaction(self, transaction):
        self.unconfirmed_transactions.append(transaction)

    def mine(self, name, age, diagnosis, doctor):
        if not self.unconfirmed_transactions:
            return False
        last_blocK = self.last_blocK

        new_block = Block(name, age, diagnosis, 
        doctor, index=last_blocK.index + 1, 
        transaction=self.unconfirmed_transactions, 
        timestamp=time.strftime('%X %x %Z'),
        previous_hash=last_blocK.hash)

        proof = self.proof_of_work(new_block)
        self.add_block(new_block, proof)
        self.unconfirmed_transactions = []
        print("mined a new block")
        return new_block.index