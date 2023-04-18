# How to Setup and Run HCP Node

This folder has many functions, we can mine (add a block to the blockchain), we can also request access to a block and send that request to a patient node. The HCP would need to have there own public_key.pem and pirvate_key.pem file to mine and decrypt data. For convience I have added both of these in the repo, although you should never share your private key with anyone, this is only for educational and demostrative purposes.

## mining
To mine a block, you can use the mine.py program. mine.py is resposible for mining a block ( for example when a doctor diagnosis a patient, they would mine there diagnosis and it would be stored on the blockchain), you need to provide the patients public key in order to encrpyt that data and add it to the blockchain. The program needs to be able to locate a file called patient_public_key.pem (provided in the repo for convience) and will use that to encrypt the data. Once you run the program (python mine.py) It will load your blockchain (stored in blockchain.pickle) and will ask you to enter the diagnosis data. Once you enter all of the data, you wull be provided with a transaction-ID (this will be a UUID for example '01783668-ebdd-4249-83cd-3f4931b2ba6a' ), this transaction-ID will also be added to the patients public_key file. A message should appear that states your blockchain has been saved.

```bash

$ pythong mine.py
Blockchain has been loaded
the host is 2001:1970:5f59:8000::72b2
Here is the hash of the last block 00dcfc41b426a6ec78247b8f658f72b00a7be8b50ccc41f2684b9625f34e168f
diagnosis:flu           
Doctor name:Dr. Steve
Symptoms:headache, rash, coughing
treatment:cough medicine and rest
prescription:Advil
b8ad75c2-8af7-4452-851a-1900e8fd9e53
MINE
Blockchain has been saved
current block hash 00feb001b834243044d7c593f163002743d2a384a1ff50c84109ef36bb3dca10

```
As you can see you will have 5 fields that allow you to enter the patients data, diagnosis, doctor name, symptoms, treatment and prescription. Once entered this data will be saved on the blockchain and a hash will be created for that block.


## sending a request to a patient to view there PHR
To make a request you first need to have a copy of a blockchain (blockchain.pickle file). You can create one by mining a block (running pythong mine.py as shown in the section above)
A health care providor can request access to a patients data, this can be conde by using 'view_block.py' program. The view_block.py program sends a request to a patient node,
the request sends the encrypted block data to the patient. The patient then decrypts that data and sends it back to the doctor for viewing.
For view_block.py to work there needs to be an active patient node before running the view_block program (patient side needs to run 'python server.py' so that it can accept the request, you can check the patient readme to learn more)

Here is how to run view_block.py
```py
$python view_block.py
```

Below the is what would be outputted to the terminal
```bash
Transaction_id:b8ad75c2-8af7-4452-851a-1900e8fd9e53
Blockchain has been loaded
the host is 2001:1970:5f59:8000::72b2
-----BEGIN PUBLIC KEY-----
MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAtg1c457aJxSeqQiyDiL6
eNmoB3WpHYmrc/xtfspKgLBiuCxG8QHuVP2EEccRHkit+S9JGEG0bkwJNQfOqvfU
jTbdRoN6ZDEYUjcIk/G4W0lXvjHIu3mdn49n3lV1ZAJtpZTM2O4H4mJ2bYYMgMRo
X0tgR3gIDP3v3RoMsN3YZ7nOX7nxKN78/v7osMuUGSPHR0V+UqcHSi/ApldNwm7F
zLjPSnR+4VWflYCOquJZumolRH6RIDnPrHWNkEOLYCGTB0a3mgZvHGyRy7IfP+S5
mAplJgaj7GmxMhkRNDlDwQztv7Z2wkUtqEO1hvoEyUDJjDbsoGeO9aZf4Gnuiamy
3fRynJj99hj8tHo/k0AE7R8XbZMb71fM5M71FzJjFjLVZ0bOuKy2ZiVWNwuwiLTE
/+GCY5aYGpe+q0zQe2iVmgOrFyn4QGF3eclcyw92Qu09G6O3ymxavsfaG9qA4mXV
HiDBog99qUMyoPfqRQMRIYqAwk/Dc32bfJct9V7R2rzMPQAc2VZGYcyCDbwtUF8Z
dQgxzwijy6EGMDuNAPsD/Hfj0ekvnf5+LzeAfLBbV0q7Je8GM7oFeDVBeSnBCTUm
SwKMMcyyNtKnmMoApNVEPNnHUCj85xmDYwBlxRO6HBw5AzSczlI2w2pyo729+dvl
nbizRpaGU8gGv3BODS3V9Q0CAwEAAQ==
-----END PUBLIC KEY-----

Signature is valid
doctor verified

id is b8ad75c2-8af7-4452-851a-1900e8fd9e53

    Diagnosis: flu
    Doctor: Dr. Steve 
    Symptoms: headache, rash, coughing
    Treatment: cough medicine and rest
    Prescription: Advil
```








