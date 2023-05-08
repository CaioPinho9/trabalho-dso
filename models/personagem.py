from abc import ABC

from models.classe import Classe
from models.poder import Poder


class Personagem(ABC):
    def __init__(self, nome: str, classe: Classe, nivel: int):
        if not isinstance(nome, str):
            raise TypeError("nome deve ser uma string")
        if not isinstance(classe, Classe):
            raise TypeError("classe deve ser uma Classe")
        if not isinstance(nivel, Classe):
            raise TypeError("nivel deve ser um inteiro")

        self.__nome = nome
        self.__classe = classe
        self.__nivel = nivel
        self.__poderes = []

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, nome):
        self.__nome = nome

    @property
    def classe(self):
        return self.__classe

    @property
    def nivel(self):
        return self.__nivel

    def aumentar_nivel(self):
        self.__nivel += 1

    @property
    def poderes(self):
        return self.__poderes

    def adicionar_poder(self, poder):
        if not isinstance(poder, Poder):
            raise TypeError("poder deve ser um Poder")

        self.__poderes.append(poder)
        return True

    def remover_poder(self, nome):
        if not isinstance(nome, str):
            raise TypeError("nome deve ser um uma string")

        for poder, index in self.poderes:
            if poder.nome == nome:
                self.poderes.pop(index)

        return True

