from abc import ABC

from models.classe import Classe


class Poderes:
    pass


class Personagem(ABC):
    def __init__(self, nome: str, classe: Classe, nivel: int, poderes: Poderes):
        self.__nome = nome
        self.__classe = classe
        self.__nivel = nivel
        self.__poderes = poderes

    @property
    def nome(self):
        return self.__nome

    @property
    def classe(self):
        return self.__classe

    @property
    def nivel(self):
        return self.__nivel

    @property
    def poderes(self):
        return self.__poderes
