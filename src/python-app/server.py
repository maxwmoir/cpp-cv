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
    """
    Class implementing the UDP server to receive coordinate datagrams from the C++ client.
    """

    def __init__(self, host = DEFAULT_HOST, port = DEFAULT_PORT):
        """
        Initialize the Server
        Args:
            host (str): Server host 
            port (int): Server port
        """
        self.host = host
        self.port = port
        self.last_packet = []
        self.sock = None 
        self.sock.bind((self.host, self.port))

    def bind_socket(self):
        """
        Create and bind the UDP socket.
        """
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        except Exception as e:
            self.shut_down()
            print("ERROR: Socket creation failed")
            print(e)
            exit()

        try:
            self.sock.bind((self.host, self.port))
        except Exception as e:
            self.shut_down()
            print("ERROR: Socket binding failed")
            print(e)
            exit()
 
        

    def start(self):
        """
        Main listening function to receive and store datagrams
        """
        print("Starting")
        while True:
            data, addr = self.sock.recvfrom(4097)
            float_array = np.frombuffer(data, dtype=np.float32)
            self.last_packet = float_array
            


    def run_async(self):
        """
        Run the main function asynchronously 
        """
        thread = threading.Thread(target=self.start)
        thread.start()

if __name__ == "__main__":
    server = Server(port=9999)
    server.run_async()
