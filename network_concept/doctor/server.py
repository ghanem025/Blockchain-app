import socket
import pickle

HOST = '0.0.0.0'
PORT = 5000 
print("Socket started")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(4096)
            if not data:
                print("there is no data")
                break
            # Process the received data here
            print("we got the data")
            data_variable = pickle.loads(data)
            print(
                f'''
                Diagnosis:{data_variable.diagnosis}
                Doctor: {data_variable.doctor}
                symptoms: {data_variable.symptoms}
                treatment: {data_variable.treatment}
                prescription: {data_variable.prescription}
                ''')
