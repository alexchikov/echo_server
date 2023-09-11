import socket
import logging
import random
import sys
from typing import ByteString

logging.basicConfig(level=logging.INFO, stream=sys.stdout,
                    format="%(levelname)s %(asctime)s: %(message)s")


class Server(object):
    def __init__(self, host: str = 'localhost', port: int = random.randint(6000, 9000)) -> None:
        self.__server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__server.bind((host, port,))
        logging.info(
            "started server on {} host and {} port".format(host, port))
        logging.info("started listen for connections")
        self.__server.listen(1)
        self.accept_connection()

    def accept_connection(self):
        self.__client = self.__server.accept()
        logging.info("client {} connected".format(self.__client[1]))

    def _receive_message(self) -> ByteString:
        data = self.__client[0].recv(1024)
        logging.info('message received from client')
        if data.decode() != '\exit':
            return data
        else:
            raise ConnectionResetError('Client disconnected')

    def _send_message(self, data: str):
        self.__client[0].send(data)

    def run(self):
        while True:
            try:
                data = self._receive_message()
                self._send_message(data)
            except ConnectionResetError:
                logging.warning('client disconnected from server')
                self.accept_connection()


if __name__ == "__main__":
    s = Server()
    s.run()
