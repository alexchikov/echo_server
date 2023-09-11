import socket
import logging
import sys

logging.basicConfig(level=logging.INFO, filename="client.log",
                    filemode='a+', format="%(levelname)s %(asctime)s: %(message)s")


class Client(object):
    def __init__(self, host: str, port: int) -> None:
        self.__client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        logging.info('setted up client')
        try:
            self.__client.connect((host, port,))
            logging.info('connected to the server')
        except ConnectionError as e:
            logging.error(e)
            sys.exit(1)

    def _send_message(self, message: str):
        self.__client.send(message.encode())
        logging.info('send data to server')
        if message == '\exit':
            logging.info('disconnected from server')
            self.__client.close()
            sys.exit(0)

    def _receive_message(self):
        logging.info('receive data from server')
        return self.__client.recv(1024).decode()

    def run(self, data: str):
        self._send_message(data)
        print(self._receive_message())


if __name__ == "__main__":
    c = Client(input('Host: '), int(input('Port: ')))
    while True:
        c.run(input('::'))
