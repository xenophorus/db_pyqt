#!/usr/bin/python3

from socket import SOCK_STREAM, AF_INET, socket
from lib.funx import *
from lib.logger import *
from lib.class_client import Message


def mainloop(address):
    with socket(AF_INET, SOCK_STREAM) as sock:
        sock.connect(address)
        while True:
            try:
                data = sock.recv(1024)
                msg = Message()
                Message.decode(self=msg, data=data)
                print(f'{msg.from_user} at {msg.time_date} said to {msg.to_user}:\n\t{msg.message}')
            except OSError as e:
                log.critical(f'Something wrong. No answer from server.\n\t\t{e}')
                sys.exit()


def main(args):
    log.info('client started')
    if len(args) > 1:
        mainloop(parse_args(args[1:]))
    else:
        mainloop(('127.0.0.1', 9090))


if __name__ == '__main__':
    main(sys.argv)
