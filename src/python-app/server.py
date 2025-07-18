"""
UDP server class
- server.py

Created: 
- 10/07/25

Author: 
- Max Moir
"""

# Package imports
import socket
import threading
import numpy as np

# Program Constants

DEFAULT_HOST = '0.0.0.0'
DEFAULT_PORT = 9999

class Server:
    def __init__(self, host = DEFAULT_HOST, port = DEFAULT_PORT):
        self.host = host
        self.port = port
        self.last_packet = []
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.host, self.port))

    def start(self):
        print("Starting")
        while True:
            data, addr = self.sock.recvfrom(4097)
            float_array = np.frombuffer(data, dtype=np.float32)
            self.last_packet = float_array
            


    def run_async(self):
        thread = threading.Thread(target=self.start)
        thread.start()

if __name__ == "__main__":
    server = Server(port=9999)
    server.run_async()
