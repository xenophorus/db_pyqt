import sys
from socket import SOCK_STREAM, AF_INET, socket
from threading import Thread

from lib.logger import log
from lib.decorators import log_dec
from lib.meta import HostVerifier, PortVerifier
from lib.class_message import Message


class Client:

    host = HostVerifier()
    port = PortVerifier()

    def __init__(self, host, port, name):
        self.host = host
        self.port = port
        self.address = (self.host, self.port,)
        self.name = name
        self.sock = self.get_sock()

    def get_sock(self):
        sock = socket(AF_INET, SOCK_STREAM)
        sock.connect(self.address)
        print(sock.getsockname()[1])
        return sock

    def send_loop(self):
        while True:
            key = input(f'Введите команду: '
                        f'"q" для выхода, '
                        f'"m" для нового сообщения:\n')
            if key == 'q':
                sys.exit()
            elif key == 'm':
                message = Message()
                message.create('message', self.name)
                self.sender(message.encode())

    def get_loop(self):
        while True:
            try:
                data = self.sock.recv(1024)
                msg = Message()
                Message.decode(self=msg, data=data)
                if msg.to_user == self.name or msg.to_user == 'all':
                    print(f'\t{msg.from_user} said to {msg.to_user} at {msg.time_date}:\n{msg.message}')
            except OSError as e:
                self.crit_log(e)

    def sender(self, msg):
        try:
            self.sock.send(msg)
            log.info(f'{msg} sent')
        except OSError as e:
            self.crit_log(e)

    def get_message(self):
        try:
            data = self.sock.recv(1024)
            msg = Message()
            Message.decode(self=msg, data=data)
            print(f'{msg.from_user} at {msg.time_date} said to {msg.to_user}:\n\t{msg.message}')
        except OSError as e:
            self.crit_log(e)

    @staticmethod
    def crit_log(err):
        log.critical(f'Something wrong. No answer from server.\n\t\t{err}')
        sys.exit()

    @log_dec
    def mainloop(self):
        thr1 = Thread(target=self.get_loop)
        thr1.start()
        self.send_loop()
