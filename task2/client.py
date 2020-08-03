import argparse

from lib.decorators import log_dec
from lib.logger import *
from lib.classes import Client


@log_dec
def main():
    parser = argparse.ArgumentParser(description='Client app')
    parser.add_argument('-p', action='store', dest='prt', type=int)
    parser.add_argument('-d', action='store', dest='ip')
    parser.add_argument('-n', action='store', dest='name')
    args = parser.parse_args()
    log.info(f'client {args.name} started')

    client = Client((args.ip, args.prt), args.name)
    # client = Client(('127.0.0.1', 9090), 'user')
    client.mainloop()


if __name__ == '__main__':
    main()
