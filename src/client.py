import pickle
import socket
import time
import uuid

from blockchain import Block
import uuid
uuidfour = uuid.uuid4()
first_block = Block(str(uuidfour) ,"flu", "Dr.Balls", "itchy ball", 
"amputation", "crack", 0, [], time.strftime('%X %x %Z'), "0") # I used time.strftime for an acurate date
HOST = '24.57.109.146'  # The server's hostname or IP address
PORT = 65432  # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(pickle.dumps(first_block))

    data = s.recv(1024)
    print('Received:', data.decode())
