import subprocess
import time

process = []

while True:
    action = input('Действие: q - выход, s - запустить сервер и клиенты, x - закрыть все: ')

    if action == 'q':
        break
    elif action == 's':
        process.append(subprocess.Popen('python server.py -d 127.0.0.1 -p 9090',
                                        creationflags=subprocess.CREATE_NEW_CONSOLE))
        for i in range(3):
            process.append(subprocess.Popen(f'python client.py -d 127.0.0.1 -p 9090 -n user{i}',  # -m send',0
                                            creationflags=subprocess.CREATE_NEW_CONSOLE))
            print(f'python client.py -d 127.0.0.1 -p 9090 -n user{i}')
            time.sleep(1)
        # for i in range(2):
        #     process.append(subprocess.Popen('python monitor.py',  # -m listen',
        #                                     creationflags=subprocess.CREATE_NEW_CONSOLE))
    elif action == 'x':
        for i in process.copy():
            proc_to_kill = process.pop()
            proc_to_kill.kill()
