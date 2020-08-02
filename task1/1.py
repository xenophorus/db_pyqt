import subprocess
from pprint import pprint

import chardet
import ipaddress
from tabulate import tabulate


# Написать функцию host_ping(), в которой с помощью утилиты ping будет проверяться доступность сетевых узлов.
# Аргументом функции является список, в котором каждый сетевой узел должен быть представлен именем хоста или
# ip-адресом. В функции необходимо перебирать ip-адреса и проверять их доступность с выводом соответствующего
# сообщения («Узел доступен», «Узел недоступен»). При этом ip-адрес сетевого узла должен создаваться с помощью
# функции ip_address().


def dec(s):
    if s:
        enc = chardet.detect(s)
        return s.decode(enc.get('encoding'))


def host_ping(*args):
    addresses = args[0]
    result = []

    for addr in addresses:
        args = ['ping', '-c 3', addr]
        proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        code = proc.wait()
        if code == 0:
            result.append({'ip': addr, 'status': 'reachable'})
        elif code == 1:
            result.append({'ip': addr, 'status': 'unreachable'})
    return result


# Написать функцию host_range_ping() для перебора ip-адресов из заданного диапазона. Меняться должен только
# последний октет каждого адреса. По результатам проверки должно выводиться соответствующее сообщение.


def host_range_ping(addr, d=0):
    addresses = []
    if d:
        for i in range(d):
            addresses.append(str(ipaddress.ip_address(addr) + i))
    else:
        addresses.append(str(ipaddress.ip_address(addr)))
    return addresses


# Написать функцию host_range_ping_tab(), возможности которой основаны на функции из примера 2. Но в данном
# случае результат должен быть итоговым по всем ip-адресам, представленным в табличном формате (использовать
# модуль tabulate). Таблица должна состоять из двух колонок и выглядеть примерно так:
# Reachable
# -------------
# 10.0.0.1
# 10.0.0.2
# Unreachable
# -------------
# 10.0.0.3
# 10.0.0.4


def host_range_ping_tab(addr):
    d = host_ping(addr)
    print(tabulate(d, headers='keys', tablefmt='pipe'))


# Продолжаем работать над проектом «Мессенджер»:

# Реализовать скрипт, запускающий два клиентских приложения: на чтение чата и на запись в него.
# Уместно использовать модуль subprocess);

# Реализовать скрипт, запускающий указанное количество клиентских приложений.


# *В следующем уроке мы будем изучать дескрипторы и метаклассы. Но вы уже сейчас можете перевести часть кода из
# функционального стиля в объектно-ориентированный. Создайте классы «Клиент» и «Сервер», а используемые функции
# превратите в методы классов.

def print_res(f, addrlist):
    lst = f(addrlist)
    for i in lst:
        print(i['ip'], 'is', i['status'])


host_list1 = ['122.254.254.12', '10.254.254.13', '192.168.1.13', '22.54.24.15', 'google.com']

print_res(host_ping, host_list1)

print_res(host_ping, host_range_ping('122.254.254.13', 4))

host_range_ping_tab(host_list1)
