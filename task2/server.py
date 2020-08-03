import argparse

from lib.classes import Server
from lib.decorators import log_dec


@log_dec
def main():
    parser = argparse.ArgumentParser(description='Server app')
    parser.add_argument('-p', action='store', dest='prt', type=int)
    parser.add_argument('-d', action='store', dest='ip')
    args = parser.parse_args()
    s = Server((args.ip, args.prt),)
    s.mainloop()


if __name__ == '__main__':
    main()
