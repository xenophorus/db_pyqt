from ipaddress import *
from socket import gethostbyname


class HostVerifier:

    def __set__(self, instance, value):  # TODO: Дополнить проверку хоста
        if type(ip_address(gethostbyname(value))) != IPv4Address:
            raise ValueError(f'Неверный хост')
        instance.__dict__[self.name] = value

    def __set_name__(self, owner, name):
        self.name = name


class PortVerifier:

    def __set__(self, instance, value):
        if type(value) != int:
            raise TypeError(f'Incorrect type. Got {type(value)} instead int')
        if not 1000 < value < 65535:
            raise ValueError(f'Port must be 1000 < value < 65535')
        instance.__dict__[self.name] = value

    def __set_name__(self, owner, name):
        self.name = name


class MyMetaClass:
    def __new__(cls, name, bases, dct):
        print(f'name: {name}\nbases: {bases}\ndct: {dct}')
        return type.__new__(type, name, bases, dct)

    def __init__(self, name, bases, dct):
        print(f'init class {name}')
        super(MyMetaClass, self).__init__(name, bases, dct)
