#!/usr/bin/python3

import argparse
import sys

from lib.classes import Server
from lib.decorators import log_dec


@log_dec
def main(*args, **kwargs):
    parser = argparse.ArgumentParser(description='Server app')
    parser.add_argument('-p', action='store', dest='prt', type=int)
    parser.add_argument('-d', action='store', dest='ip')
    args = parser.parse_args()
    ip = str(args.ip).strip()
    # s = Server(ip, args.prt,)
    s = Server('127.0.0.1', 9090,)
    s.mainloop()


if __name__ == '__main__':
    main(sys.argv)
