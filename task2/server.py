import argparse
import select

from socket import SOCK_STREAM, AF_INET, socket

from lib.classes import Server
from lib.decorators import log_dec
from lib.funx import *
from lib.logger import *

#
# def read_requests(r_clients, all_clients):
#     responses = {}
#     for sock in r_clients:
#         try:
#             data = sock.recv(1024)
#             responses[sock] = data.decode('utf-8')
#             log.debug(f'data = {responses[sock]}')
#         except Exception as e:
#             log.error(f'Клиент {sock.fileno()} {sock.getpeername()} отключился\n\t\t{e}')
#             all_clients.remove(sock)
#     return responses
#
#
# def write_responses(requests, w_clients, all_clients):
#     for sock in all_clients:
#         if sock in requests:
#             print(f'{requests}\n{w_clients}\n{all_clients}\n\n\n')
#             try:
#                 resp = requests[sock].encode('utf-8')
#
#                 for i in w_clients:
#                     i.send(resp)
#             except Exception as e:
#                 print(e)
#                 log.error(f'Клиент {sock.fileno()} {sock.getpeername()} отключился\n\t\t{e}')
#                 sock.close()
#                 all_clients.remove(sock)
#
#
# @log_dec
# def mainloop(address):
#     clients = []
#     s = socket(AF_INET, SOCK_STREAM)
#     s.bind(address)
#     s.listen(5)
#     s.settimeout(1)
#
#     while True:
#         try:
#             conn, addr = s.accept()
#         except OSError as e:
#             # log.error(f'{e}')
#             pass
#         else:
#             print("Получен запрос на соединение с %s" % str(addr))
#             log.info(f'Получен запрос на соединение с {str(addr)}')
#             clients.append(conn)
#             print(clients)
#         finally:
#             wait = 50
#             r = []
#             w = []
#             try:
#                 r, w, e = select.select(clients, clients, [], wait)
#             except Exception as e:
#                 # log.error(f'{e}')
#                 pass
#
#             requests = read_requests(r, clients)
#             if requests:
#                 write_responses(requests, w, clients)


@log_dec
def main():
    parser = argparse.ArgumentParser(description='Server app')
    parser.add_argument('-p', action='store', dest='prt', type=int)
    parser.add_argument('-d', action='store', dest='ip')
    args = parser.parse_args()
    # mainloop((args.ip, args.prt),)
    s = Server(('127.0.0.1', 9090),)
    s.mainloop()


if __name__ == '__main__':
    main()
