import subprocess

process = []

while True:
    action = input('Действие: q - выход, s - запустить сервер и клиенты, x - закрыть все: ')

    if action == 'q':
        break
    elif action == 's':
        process.append(subprocess.Popen('python server.py -d 127.0.0.1 -p 9090', shell=True,
                                        creationflags=subprocess.CREATE_NEW_CONSOLE))
        for i in range(3):
            process.append(subprocess.Popen(f'python client.py -d 127.0.0.1 -p 9090 -n user{i}',
                                            shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE))
        # for i in range(2):
        #     process.append(subprocess.Popen('python monitor.py', shell=True))
    elif action == 'x':
        for i in process.copy():
            proc_to_kill = process.pop()
            proc_to_kill.kill()
