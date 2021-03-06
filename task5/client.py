#!/usr/bin/python3

import argparse

import hashlib
from threading import Thread
from lib.names import human_name
from lib.decorators import log_dec
from lib.class_client import Client


@log_dec
def main():
    parser = argparse.ArgumentParser(description='Client app')
    parser.add_argument('-p', action='store', dest='prt', type=int)
    parser.add_argument('-d', action='store', dest='ip')
    parser.add_argument('-n', action='store', dest='name')
    parser.add_argument('-s', action='store', dest='password')
    args = parser.parse_args()
    ip = str(args.ip).strip()
    # name = str(args.name).strip()
    name = human_name()
    password = 'qwerty'
    # hex_id = hashlib.sha1(f'{str(args.name).strip()}@{str(args.password).strip()}'.encode('utf-8')).hexdigest()
    hex_id = hashlib.sha1(f'{name}@{password}'.encode('utf-8')).hexdigest()

    # client = Client(ip, args.prt, name, hex_id)
    client = Client('127.0.0.1', 9090, name, hex_id)

    thr1 = Thread(target=client.get_loop)
    thr1.start()
    client.send_loop()


if __name__ == '__main__':
    main()
