import pickle
from abc import ABC, abstractmethod

from exceptions import exceptions


class DAO(ABC):
    @abstractmethod
    def __init__(self, datasource=''):
        self.__datasource = datasource
        self.__cache = {}
        try:
            self.__load()
        except FileNotFoundError:
            self.__dump()

    def __dump(self):
        pickle.dump(self.__cache, open(self.__datasource, 'wb'))

    def __load(self):
        self.__cache = pickle.load(open(self.__datasource, 'rb'))

    def add(self, key, obj):
        self.__cache[key] = obj
        self.__dump()

    def update(self, key, obj):
        if key in self.__cache:
            self.__cache[key] = obj
            self.__dump()
        else:
            raise exceptions.NaoEncontradoException("Key não encontrada")

    def get(self, key):
        if key in self.__cache:
            return self.__cache[key]
        raise exceptions.NaoEncontradoException("Key não encontrada")

    def remove(self, key):
        if key not in self.__cache:
            raise exceptions.NaoEncontradoException("Key não encontrada")
        self.__cache.pop(key)
        self.__dump()

    def get_all(self):
        return list(self.__cache.values())
