def show_help():
    print('Possible parameters:'
          '\n\t-h: host'
          '\n\t-p: port'
          '\n\t-? or help: show this help'
          '\n\t default host:port is 127.0.0.1:9090')


def parse_args(args):
    host, port, name = '127.0.0.1', 9090, 'user'

    for i in range(len(args)):
        if args[i] == '-p':
            port = args[i + 1]
        elif args[i] == '-h':
            host = args[i + 1]
        elif args[i] == '-n':
            name = args[i + 1]
        elif args[i] == '-?':
            show_help()
            break
        else:
            if i % 2 == 0:
                print(f'{args[i]} is incorrect argument. Skipped')
    addr = (host, port)
    return [addr, name]
