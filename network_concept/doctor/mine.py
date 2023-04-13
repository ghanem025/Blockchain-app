from blockchain import Blockchain, Block
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
import base64
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
with open('patient_public_key.pem', 'r') as f:
    public_key_data = f.read()
import uuid
uuidOne = uuid.uuid4() 
public_key = serialization.load_pem_public_key(public_key_data.encode())
public_key_data = public_key_data + str(uuidOne) + '\n'

diagnosis = input("diagnosis:")
doctor = input("Doctor name:")
symptoms = input("Symptoms:")
treatment = input("treatment:")
prescription = input("prescription:")

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
print(str(uuidFour))
new_block = Block(str(uuidFour) ,diagnosis, doctor, 
symptoms, treatment, prescription,last_block.index + 1,
transaction, time.strftime('%X %x %Z'), last_block.hash) # I used time.strftime for an acurate date

b.add_new_transaction(new_block)
print("current block hash", new_block.hash)
