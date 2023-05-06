from abc import ABC, abstractmethod
from random import random

from models.poder import Poder


class ControllerPersonagem(ABC):
    def __init__(self):
        self.__personagens = []

    @abstractmethod
    def cadastrar_personagem(self, nome, nivel, poderes):
        pass

    @abstractmethod
    def remover_personagem(self, nome):
        pass

    @property
    def personagens(self):
        return self.__personagens

    def get_personagem(self, nome):
        """
        Obtém um personagem da lista de personagens.

        Parâmetros:
        nome (str): nome do Personagem a ser encontrado.

        Retorno:
        Personagem: objeto Personagem com o mesmo nome, caso encontrado; ou None, caso não encontrado.
        """
        for personagem in self.__personagens:
            if personagem.nome == nome:
                return personagem
        return None

    def calcular_ataque(self, poder: Poder):
        if not isinstance(poder, Poder):
            raise TypeError("O ataque deve ser um poder")

        random_number = random.randint(1, 20)


