import random
from abc import ABC

from models.classe import Classe
from models.poder import Poder


class Personagem(ABC):
    def __init__(self, nome: str, classe: Classe, nivel: int):
        if not isinstance(nome, str):
            raise TypeError("nome deve ser uma string")
        if not isinstance(classe, Classe):
            raise TypeError("classe deve ser uma Classe")
        if not isinstance(nivel, int):
            raise TypeError("nivel deve ser um inteiro")

        self.__nome = nome
        self.__classe = classe
        self.__nivel = nivel
        self.__poderes = []

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, nome: str):
        if not isinstance(nome, str):
            raise TypeError("nome deve ser uma string")
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

    def adicionar_poder(self, poder: Poder):
        if not isinstance(poder, Poder):
            raise TypeError("poder deve ser um Poder")

        self.__poderes.append(poder)
        return True

    def remover_poder(self, nome: str):
        if not isinstance(nome, str):
            raise TypeError("nome deve ser um uma string")

        for index, poder in enumerate(self.__poderes):
            if poder.nome == nome:
                self.poderes.pop(index)
                return True
        else:
            return False

    def calcular_poder(self, poder):
        if not isinstance(poder, Poder):
            raise TypeError("ataque deve ser um Poder")

        rolagem_jogador = random.randint(1, 20)
        resultado_acerto = rolagem_jogador + poder.acerto

        dano = 0
        # Verifica se o ataque acertou ou falhou
        if resultado_acerto >= 15:
            # Calcula o dano
            dano_minimo = round(poder.dano * 0.5)
            dano_maximo = round(poder.dano * 1.5)
            dano = int(random.randint(dano_minimo, dano_maximo))

        return dano, resultado_acerto



