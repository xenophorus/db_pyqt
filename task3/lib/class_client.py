import sys
from socket import SOCK_STREAM, AF_INET, socket

from lib.logger import log
from lib.decorators import log_dec
from lib.meta import HostVerifier, PortVerifier
from lib.class_message import Message
from lib.db_client import *


class Client:

    host = HostVerifier()
    port = PortVerifier()

    @log_dec
    def __init__(self, host, port, name, hex_id):
        self.host = host
        self.port = port
        self.address = (self.host, self.port,)
        self.name = name
        self.hex_id = hex_id
        self.sock = self.get_sock()
        self.introduce()

    def introduce(self):
        m = Message()
        m.create_info('auth_info', self.name, self.hex_id, self.sock.getsockname())
        self.sender(m)
        print('auth sent')

    def get_sock(self):
        sock = socket(AF_INET, SOCK_STREAM)
        sock.connect(self.address)
        print(sock.getsockname()[1])
        return sock

    def send_loop(self):
        while True:
            key = input(f'Введите команду: '
                        f'"q" для выхода, '
                        f'"w" - who am i, '
                        f'"m" для нового сообщения:\n')

            if key == 'q':
                sys.exit()
            elif key == 'm':
                message = Message()
                message.create('message', self.name)
                self.sender(message)
            elif key == 'w':
                print(f'I am {self.name} from ip {self.host}')

    def sender(self, msg):
        try:
            self.sock.send(msg.encode())
            print('msg sent: ', msg.__dict__())
            log.info(f'{msg} sent')
        except OSError as e:
            self.crit_log(e)

    def get_loop(self):
        while True:
            try:
                data = self.sock.recv(1024)
                msg = Message()
                print('msg:  ', msg)
                msg.decode(data)
                # if msg.action == 'message':
                # print(f'{msg.from_user} at {msg.time_date} said to {msg.to_user}:\n\t{msg.message}')
                db_add_message(msg.from_user, msg.to_user, msg.time_date, msg.message)
                print(f'{msg.from_user} at {msg.time_date} said to {msg.to_user}:\n\t{msg.message}')
            except OSError as e:
                self.crit_log(e)

    def crit_log(self, err):
        log.critical(f'Something wrong. No answer from server.\n\t\t{err}')
        sys.exit()
