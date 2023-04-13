from blockchain import *
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

with open('public_key.pem', 'r') as f:
    public_key_data = f.read()

transaction_id = input("transaction_id:")

with open('private_key.pem', 'r') as f:
    private_key_data = f.read()
private_key = serialization.load_pem_private_key(private_key_data.encode(), password=None)

message = b'I am Dr. Balls I would like to view your PHR plz'
signature = private_key.sign(
    message,
    padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),
        salt_length=padding.PSS.MAX_LENGTH
    ),
    hashes.SHA256()
)

b = Blockchain()
contract = b.SmartContract()

if contract.check_signature(public_key_data, signature, message):
    print("doctor verified")
    data = b.send_request(transaction_id, public_key_data)
    decoded = data.decode()
    block_data = json.loads(decoded)

    fields = ['diagnosis', 'doctor', 'symptoms', 'treatment', 'prescription']
    import base64
    for values in fields:
        block_data[values] = private_key.decrypt(
            base64.b64decode(block_data[values]),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        ).decode('utf-8')
    print(
        f'''
          Diagnosis: {block_data['diagnosis']}
          Doctor: {block_data['doctor']} 
          Symptoms: {block_data['symptoms']}
          Treatment: {block_data['treatment']}
          Prescription: {block_data['prescription']}
        '''
    )

