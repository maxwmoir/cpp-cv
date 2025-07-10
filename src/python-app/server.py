# udp_server.py
import socket
import threading
import numpy as np

class UDPServer:
    def __init__(self, host='0.0.0.0', port=9999):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.host, self.port))
        print(f"Server listening on {self.host}:{self.port}")

    def start(self):
        print("Waiting for messages...")
        while True:
            data, addr = self.sock.recvfrom(4096)
            float_array = np.frombuffer(data, dtype=np.float32)
            print(f"Received from {addr}: {float_array}")
            

    def run_async(self):
        thread = threading.Thread(target=self.start)
        thread.daemon = True
        thread.start()

if __name__ == "__main__":
    server = UDPServer(port=9999)
    server.start()
