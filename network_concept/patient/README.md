# How to Setup and Run Patient Node

To run the patient node, you just need to run python server.py.

```bash
$ python server.py
```
This program will wait for a request from a doctor, once a request is sent the patient side will use a smart contract to check if the doctor is authorized. This authorization is done using the patients 'authorized_doctors' folder. This folder should hold the public keys of all the doctors that the patient gave permission to access there data. once the verification process is completed the patient will decrypt the data, encrypt it with the doctors public key and send it back to the doctor.

```bash
$ python server.py

Socket started
Connected by ('127.0.0.1', 47474)
Block data received
Blockchain has been loaded
the host is 2001:1970:5f59:8000::72b2
Signature is valid
there is no data
```
This is what your output should look like when you connect to a doctor and send them the data correctly. The doctor should receive the data and be able to decypt and read it.
