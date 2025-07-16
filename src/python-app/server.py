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

class UDPServer:
    def __init__(self, host='0.0.0.0', port=9999):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.host, self.port))
        self.array = []

    def start(self):
        count = 0
        while True:
            data, addr = self.sock.recvfrom(4097)
            float_array = np.frombuffer(data, dtype=np.float32)
            count += 1
            self.array = float_array

    def run_async(self):
        thread = threading.Thread(target=self.start)
        thread.start()

if __name__ == "__main__":
    server = UDPServer(port=9999)
    server.run_async()
