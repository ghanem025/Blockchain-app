from blockchain import Blockchain, Block
import uuid
import time

b = Blockchain.create()
last_block = b.last_block
print("Here is the hash of the last block", last_block.hash)

uuidFour = uuid.uuid4()

transaction = {
    'sender': 'Dr. Deez',
    'recipient': str(uuidFour)
}
new_block = Block(str(uuidFour) ,"flu", "Dr.Deez", 
"itchy ball", "amputation", "cracksssss",last_block.index + 1,
transaction, time.strftime('%X %x %Z'), last_block.hash) # I used time.strftime for an acurate date

b.add_new_transaction(new_block)
print("current block hash", new_block.hash)
