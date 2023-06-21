import os
import pickle
from abc import ABC, abstractmethod

from exceptions import exceptions


class DAO(ABC):
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @abstractmethod
    def __init__(self, datasource=''):
        self.__datasource = datasource
        self.__cache = {}
        self.__last_index = self.__load_last_index()
        try:
            self.__load()
        except FileNotFoundError:
            self.__dump()

    def __dump(self):
        with open(self.__datasource, 'wb') as file:
            pickle.dump((self.__cache, self.__last_index), file)

    def __load(self):
        with open(self.__datasource, 'rb') as file:
            self.__cache, self.__last_index = pickle.load(file)

    def __load_last_index(self):
        if os.path.exists(self.__datasource):
            with open(self.__datasource, 'rb') as file:
                try:
                    _, last_index = pickle.load(file)
                    return last_index
                except (pickle.UnpicklingError, IndexError):
                    pass
        return -1

    def add(self, key, obj):
        self.__cache[key] = obj
        self.__last_index += 1
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

    def get_next_index(self):
        return self.__last_index + 1

    def clear_file(self):
        self.__cache = {}
        self.__last_index = -1
        self.__dump()
