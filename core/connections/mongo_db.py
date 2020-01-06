"""
Padrão de projeto singleton
"""
from pymongo import MongoClient


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
            self.connection = MongoClient('192.168.99.100', 27017)
        return self.connection
