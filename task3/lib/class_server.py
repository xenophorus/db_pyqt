import select
from socket import SOCK_STREAM, AF_INET, socket

from lib.logger import log
from lib.decorators import log_dec
from lib.meta import HostVerifier, PortVerifier, ServerMetaClass
from lib.class_message import Message
from lib.db_server import *


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

                print('responses: ', responses)
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
    def auth_request(self, conn):
        msg = Message()
        msg.create_info('auth_request', '', '', '')
        conn.send(msg.encode())
        print("addr: ", conn)

    def auth(self, sock):
        data = sock.recv(1024)
        msg = Message()
        msg.decode(data)
        print('resp = ', msg)
        if msg.action == 'auth_info':
            name = msg.from_user
            uid = msg.to_user
            uip = msg.message[0]
            db_user_add((name, uid, uip, True,))

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
                self.auth_request(conn)
                self.auth(conn)

                self.clients.append(conn)
                print(self.clients)
            finally:
                wait = 1.0
                r = []
                w = []
                try:
                    r, w, e = select.select(self.clients, self.clients, [], wait)
                except Exception:
                    pass

                requests = self.read_requests(r)
                if requests:
                    self.write_responses(requests, w)
