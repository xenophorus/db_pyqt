import select
from socket import SOCK_STREAM, AF_INET, socket

from lib.class_message import Message
from lib.db_server import *
from lib.decorators import log_dec
from lib.logger import log
from lib.meta import HostVerifier, PortVerifier, ServerMetaClass


class Server(metaclass=ServerMetaClass):
    host = HostVerifier()
    port = PortVerifier()

    def __init__(self, host, port):
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.host = host
        self.port = port
        self.clients = []

    def echo(self, r_clients, w_clients):
        # def read_requests(self, r_clients):
        responses = {}
        for sock in r_clients:
            try:
                data = sock.recv(1024)
                m = Message()
                m.decode(data)
                responses[sock] = m
                print('Message received', m)
                log.debug(f'data = {responses[sock]}')
            except Exception as e:
                self.client_disconnect(e, sock)

            try:
                if responses[sock]:
                    print('responses: ', responses)
                    if responses[sock].action == 'auth_info':
                        self.auth(responses[sock].__dict__())
                    elif responses[sock].action == 'info_request':
                        self.send_info()
                    elif responses[sock].action == 'message':
                        self.write_responses(responses[sock], w_clients)
            except KeyError:
                print('Client disconnected')

    def write_responses(self, msg, w_clients):
        to_user = msg.to_user
        if to_user == 'all':
            for sock in self.clients:
                try:
                    for i in w_clients:
                        i.send(msg.encode())
                except Exception as e:
                    self.client_disconnect(e, sock)
        else:
            uip = db_user_ip(to_user)
            for sock in self.clients:
                if self.str_pair(sock.getpeername()) == uip:
                    try:
                        sock.send(msg.encode())

                    except Exception as e:
                        self.client_disconnect(e, sock)

    def client_disconnect(self, err, sock):
        log.info(f'Клиент {sock.fileno()} {sock.getpeername()} отключился\n\t\t{err}')
        db_change_user_activity(self.str_pair(sock.getpeername()))
        sock.close()
        self.clients.remove(sock)

    def send_info(self):
        print('info request received')

    def str_pair(self, pair):
        return f'{pair[0]},{pair[1]}'

    def auth(self, msg):
        name = msg['from_user']
        uid = msg['to_user']
        uip = self.str_pair(msg['message'])
        if not db_user_in(name):
            db_user_add((name, uid, uip, True,))

    @log_dec
    def mainloop(self):
        self.sock.bind((self.host, self.port,))
        self.sock.listen(5)
        self.sock.settimeout(0.1)
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
                wait = 1.0
                r = []
                w = []
                try:
                    r, w, e = select.select(self.clients, self.clients, [], wait)
                except Exception:
                    pass

                self.echo(r, w)

                # requests = self.read_requests(r)
                #
                # if requests:
                #     self.write_responses(requests, w)
