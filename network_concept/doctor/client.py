from blockchain import Blockchain, Block
import time
import uuid
import pickle

c = Blockchain()
last_block = c.last_block
print("Here is the hash of the last block", last_block.hash)
uuidFour = uuid.uuid4()
transaction = {
    'sender': 'Dr. test',
    'recipient': uuidFour
}
first_block = Block(str(uuidFour) ,"flu", "Dr. test", 
"headache", "sleep", "test", last_block.index + 1, transaction, 
time.strftime('%X %x %Z'), last_block.hash) # I used time.strftime for an acurate date
# serialized_data = pickle.dumps(first_block)

c.send_block(first_block)



