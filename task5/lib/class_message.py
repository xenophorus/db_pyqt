import json
import time


class Message:
    def __init__(self):
        self.action = 'message'
        self.from_user = 'user'
        self.to_user = ''
        self.time_date = time.asctime()
        self.message = ''

    def __repr__(self):
        return f'Message from {self.from_user} to {self.to_user}, ' \
               f'action: {self.action}, date: {self.time_date}\n ' \
               f'message: {self.message}'

    @staticmethod
    def _jsoncode(msg, command):
        if command == 'dec':
            return json.loads(msg.decode('utf-8'))
        if command == 'enc':
            return json.dumps(msg.__dict__()).encode('utf-8')

    def set_to(self):
        self.to_user = input('Введите имя: \n')

    def _set_msg(self):
        self.message = input('Введите сообщение: \n')

    def create_info(self, action, from_user, to_user, msg):
        self.action = action
        self.time_date = time.asctime()
        self.from_user = from_user
        self.to_user = to_user
        self.message = msg

    def create(self, action, from_user):
        self.action = action
        self.time_date = time.asctime()
        self.from_user = from_user
        self.set_to()
        self._set_msg()

    def decode(self, data):
        d_data = self._jsoncode(data, 'dec')
        self.action = d_data.get('action')
        self.time_date = d_data.get('time_date')
        self.to_user = d_data.get('to_user')
        self.from_user = d_data.get('from_user')
        self.message = d_data.get('message')

    def __dict__(self):
        return dict(action=self.action, time_date=self.time_date, to_user=self.to_user,
                    from_user=self.from_user, message=self.message)

    def encode(self):
        return self._jsoncode(self, 'enc')

    def values(self):
        return [self.action, self.time_date, self.from_user, self.to_user, self.message]

    def message_str(self):
        return self.message
