import random
from abc import ABC

from exceptions.exceptions import ManaInsuficienteException, DuplicadoException
from models.classe import Classe
from models.poder import Poder


class Personagem(ABC):
    def __init__(self, nome: str, classe: Classe):
        if not isinstance(nome, str):
            raise TypeError("nome deve ser uma string")
        if not isinstance(classe, Classe):
            raise TypeError("classe deve ser uma Classe")

        self.__nome = nome
        self.__classe = classe
        self.__poderes = [Poder("Soco", 0, 1, 0, 1, True, 0)]
        self.__vida_atual = classe.vida
        self.__mana_atual = classe.mana

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
    def poderes(self):
        return self.__poderes

    def get_poder(self, nome: str):
        if not isinstance(nome, str):
            raise TypeError("nome deve ser uma string")

        for poder in self.__poderes:
            if poder.nome == nome:
                return poder
        return None

    def adicionar_poder(self, poder: Poder):
        if not isinstance(poder, Poder):
            raise TypeError("poder deve ser um Poder")

        if self.get_poder(poder.nome):
            raise DuplicadoException('Não foi possivel criar a classe pois ja existe uma com o mesmo nome')

        self.__poderes.append(poder)
        return True

    def remover_poder(self, nome: str):
        if not isinstance(nome, str):
            raise TypeError("nome deve ser um uma string")

        for index, poder in enumerate(self.__poderes):
            if poder.nome == nome:
                self.__poderes.pop(index)
                return True
        else:
            return False

    @property
    def vida_atual(self):
        return self.__vida_atual

    def restaurar_vida_atual(self):
        self.__vida_atual = self.classe.vida

    def mudar_vida_atual(self, valor):
        self.__vida_atual -= valor

        if self.__vida_atual > self.__classe.vida:
            self.__vida_atual = self.__classe.vida
        elif self.__vida_atual < 0:
            self.__vida_atual = 0

    @property
    def mana_atual(self):
        return self.__mana_atual

    def restaurar_mana_atual(self):
        self.__mana_atual = self.classe.mana

    def gastar_mana(self, valor):
        if self.__mana_atual - valor < 0:
            raise ManaInsuficienteException("O Personagem não possui mana suficiente para esse poder")

        self.__mana_atual -= valor
