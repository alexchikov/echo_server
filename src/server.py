import socket
import logging
import random
import sys
import redis
import yaml
import json
from typing import ByteString
from paths import Paths as p

logging.basicConfig(level=logging.INFO, stream=sys.stdout,
                    format="%(levelname)s %(asctime)s: %(message)s")


# класс сервера
class Server(object):


    def __init__(self, host: str = 'localhost', port: int = random.randint(6000, 9000)) -> None:
        with open(p.CONFIG_PATH) as file:
            config_file = yaml.safe_load(file)
            DB_HOST = config_file['HOST']
            DB_PORT = config_file['PORT']
            DB_NAME = config_file['NAME']
            DB_PASSWORD = config_file['PASSWORD']
        self.__server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__server.bind((host, port,))
        logging.info(
            "started server on {} host and {} port".format(host, port))
        logging.info("started listen for connections")
        self.__server.listen(1)
        self.__redis_client = redis.Redis(host=DB_HOST,
                                          port=DB_PORT,
                                          db=DB_NAME)
        self.accept_connection()


    def accept_connection(self):
        self.__client = self.__server.accept()
        self.__client_username = json.loads(
                self.__client[0].recv(1024).decode())['username']
        if self.__redis_client.get(self.__client_username) is None:
            self.__redis_client.set(name=self.__client_username, 
                                    value=self.__client[1][0])
            self.__client[0].send(f'Welcome, {self.__client_username}'.encode())
        else:
            self.__client[0].send(f'Hello, {self.__client_username}'.encode())
        logging.info("client {} connected".format(self.__client[1][0]))

    # получение сообщения
    def _receive_message(self) -> ByteString:
        data = self.__client[0].recv(1024)
        logging.info('message received from client')
        if data.decode() != '\exit':
            return data
        else:
            raise ConnectionResetError('Client disconnected')

    # отправка сообщения
    def _send_message(self, data: str):
        self.__client[0].send(data)

    # запуск сервера
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
