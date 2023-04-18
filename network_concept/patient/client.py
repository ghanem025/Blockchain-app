from blockchain import Blockchain, Block
import time
import uuid


c = Blockchain()
last_block = c.last_block
print("Here is the hash of the last block", last_block.hash)
uuidFour = uuid.uuid4()
transaction = {
    'sender': 'Dr. balls',
    'recipient': uuidFour
}
first_block = Block(str(uuidFour) ,"flu", "Dr.Balls", 
"itchy ball", "death", "cracksssss", last_block.index + 1, c.unconfirmed_transactions.append(transaction), 
time.strftime('%X %x %Z'), last_block.hash) # I used time.strftime for an acurate date

c.send_block(first_block)



