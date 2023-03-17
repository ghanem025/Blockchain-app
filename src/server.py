import pickle
import socket

HOST = '104.245.146.60' 
PORT = 65432  
print("Socket started")
   
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            # Process the received data here
            data_variable = pickle.loads(data)
            print(
                f'''
                Diagnosis:{data_variable.diagnosis}
                Doctor: {data_variable.doctor}
                symptoms: {data_variable.symptoms}
                treatment: {data_variable.treatment}
                prescription: {data_variable.prescription}
                ''')
            proof_of_work = True
            if proof_of_work:
                # add to block chain, broad cast to nodes
                msg = "broadcasting message: Your block is valid and will be added to the blockchain, other nodes will be notified"
                
            else:
                msg = "Your block is invalid and will not be added to the block"
            conn.sendall(bytes(msg, 'utf-8'))
