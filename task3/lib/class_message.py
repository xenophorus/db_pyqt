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
        return f'Message from {self.from_user} to {self.to_user},' \
               f'action: {self.action}, date: {self.time_date}\n' \
               f'message: {self.message}'

    @staticmethod
    def _jsoncode(msg, command):
        if command == 'dec':
            return json.loads(msg.decode('utf-8'))
        if command == 'enc':
            return json.dumps(msg.to_dict()).encode('utf-8')

    def set_to(self):
        self.to_user = input('Введите имя: \n')

    def _set_msg(self):
        self.message = input('Введите сообщение: \n')

    def create(self, action, from_user):
        self.action = action
        self.time_date = time.asctime()
        self.from_user = from_user
        self.set_to()
        self._set_msg()
        return dict(action=self.action, time=self.time_date, to=self.to_user,
                    from_user=self.from_user, message=self.message)

    def decode(self, data):
        d_data = self._jsoncode(data, 'dec')
        self.action = d_data.get('action')
        self.time_date = d_data.get('time')
        self.to_user = d_data.get('to')
        self.from_user = d_data.get('from_user')
        self.message = d_data.get('message')
        return dict(action=self.action, time=self.time_date, to=self.to_user,
                    from_user=self.from_user, message=self.message)

    def encode(self):
        return self._jsoncode(self, 'enc')

    def values(self):
        return [self.action, self.time_date, self.from_user, self.to_user, self.message]

    def message_str(self):
        return self.message

    def to_dict(self):
        return dict(action=self.action, time=self.time_date, to=self.to_user,
                    from_user=self.from_user, message=self.message)
