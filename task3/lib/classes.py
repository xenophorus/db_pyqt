import json
import select
import sys
import time
from socket import SOCK_STREAM, AF_INET, socket
from threading import Thread

from lib.logger import log
from lib.decorators import log_dec
from lib.meta import HostVerifier, PortVerifier, ServerMetaClass


class Message:
    def __init__(self):
        self.action = 'message'
        self.from_user = 'user'
        self.to_user = ''
        self.time_date = time.asctime()
        self.message = ''

    def __repr__(self):
        return f'Message from {self.from_user} to {self.to_user},' \
               f'action: {self.action}, date: {self.time_date}\n' \
               f'message: {self.message}'

    @staticmethod
    def _jsoncode(msg, command):
        if command == 'dec':
            return json.loads(msg.decode('utf-8'))
        if command == 'enc':
            return json.dumps(msg.to_dict()).encode('utf-8')

    def set_to(self):
        self.to_user = input('Введите имя: \n')

    def _set_msg(self):
        self.message = input('Введите сообщение: \n')

    def create(self, action, from_user):
        self.action = action
        self.time_date = time.asctime()
        self.from_user = from_user
        self.set_to()
        self._set_msg()
        return dict(action=self.action, time=self.time_date, to=self.to_user,
                    from_user=self.from_user, message=self.message)

    def decode(self, data):
        d_data = self._jsoncode(data, 'dec')
        self.action = d_data.get('action')
        self.time_date = d_data.get('time')
        self.to_user = d_data.get('to')
        self.from_user = d_data.get('from_user')
        self.message = d_data.get('message')
        return dict(action=self.action, time=self.time_date, to=self.to_user,
                    from_user=self.from_user, message=self.message)

    def encode(self):
        return self._jsoncode(self, 'enc')

    def values(self):
        return [self.action, self.time_date, self.from_user, self.to_user, self.message]

    def message_str(self):
        return self.message

    def to_dict(self):
        return dict(action=self.action, time=self.time_date, to=self.to_user,
                    from_user=self.from_user, message=self.message)


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
            key = input(f'Введите команду: "q" для выхода, "m" для нового сообщения:\n')
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

    def __introduce(self):
        msg = Message()
        msg.create('introduce', self.name)
        self.sender(msg.encode())

    @staticmethod
    def crit_log(err):
        log.critical(f'Something wrong. No answer from server.\n\t\t{err}')
        sys.exit()

    def mainloop(self):
        self.__introduce()
        thr1 = Thread(target=self.get_loop)
        thr1.start()
        self.send_loop()


class Server(metaclass=ServerMetaClass):

    host = HostVerifier()
    port = PortVerifier()

    def __init__(self, host, port):
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.host = host
        self.port = port
        self.address = (self.host, self.port,)
        self.clients = []
        self.names = []

    def read_requests(self, r_clients):
        responses = {}
        for sock in r_clients:
            try:
                data = sock.recv(1024)
                responses[sock] = data.decode('utf-8')
                print(r_clients, responses)
                log.debug(f'data = {responses[sock]}')
            except Exception as e:
                log.error(f'Клиент {sock.fileno()} {sock.getpeername()} отключился\n\t\t{e}')
                self.clients.remove(sock)
        return responses

    def write_responses(self, requests, w_clients):
        for sock in self.clients:
            if sock in requests:
                try:
                    resp = requests[sock].encode('utf-8')

                    for i in w_clients:
                        i.send(resp)
                except Exception as e:
                    log.error(f'Клиент {sock.fileno()} {sock.getpeername()} отключился\n\t\t{e}')
                    sock.close()
                    self.clients.remove(sock)

    @log_dec
    def mainloop(self):
        print(self.sock, self.address)
        self.sock.bind(self.address)
        self.sock.listen(5)
        self.sock.settimeout(0.2)
        while True:
            try:
                conn, addr = self.sock.accept()
            except OSError:
                pass
            else:
                print("Получен запрос на соединение с %s" % str(addr))
                log.info(f'Получен запрос на соединение с {str(addr)}')
                self.clients.append(conn)
                print(self.clients)
            finally:
                wait = 50
                r = []
                w = []
                try:
                    r, w, e = select.select(self.clients, self.clients, [], wait)
                except Exception:
                    pass

                requests = self.read_requests(r)
                if requests:
                    self.write_responses(requests, w)
