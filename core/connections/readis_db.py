"""
Padrão de projeto singleton
"""

import redis

class MetaConnect(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(MetaConnect, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Database(metaclass=MetaConnect):
    connection = None

    def connect(self):
        if self.connection is None:
            self.connection = redis(host='localhost', port=6379, db=0, password='Redis2019!')
        return self.connection