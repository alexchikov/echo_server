import socket
import logging
import sys

class Client(object):
    def __init__(self, host: str, port: int) -> None:
        self.__client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__client.connect((host, port,))
        
    def _send_message(self, message: str):
        self.__client.send(message.encode())
        if message == '\exit':
            self.__client.close()
            sys.exit(0)
        
    def _receive_message(self):
        return self.__client.recv(1024).decode()
    
    def run(self, data: str):
        self._send_message(data)
        print(self._receive_message())
    
if __name__ == "__main__":
    c = Client(input('Host: '), int(input('Port: ')))
    while True:
        c.run(input('::'))
        