chain_data = []

def decrypt_data(temp_dict, field):
        with open('private_key.pem', 'r') as f:
            private_key_data = f.read()
        try:
            private_key = serialization.load_pem_private_key(private_key_data.encode(), password=None)
        except ValueError:
            print("cannot read file it is not .pem format")
        temp_dict[field] = private_key.decrypt(
            base64.b64decode(temp_dict[field]),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        ).decode('utf-8')
        return temp_dict
        
