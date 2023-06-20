import random
from abc import ABC

from exceptions.exceptions import DuplicadoException
from models.classe import Classe
from models.poder import Poder


class Personagem(ABC):
    CODIGO = 0

    def __init__(self, nome: str, classe: Classe, poderes=None):
        if poderes is None:
            poderes = []
        if not isinstance(nome, str):
            raise TypeError("nome deve ser uma string")
        if not isinstance(classe, Classe):
            raise TypeError("classe deve ser uma Classe")
        if not all(isinstance(poder, Poder) for poder in poderes) and poderes != []:
            raise TypeError("poderes deve ser do tipo list[Poder]")

        self.__nome = nome
        self.__classe = classe
        self.__poderes = poderes
        self.__vida_atual = classe.vida
        self.__mana_atual = classe.mana
        self.__codigo = self.CODIGO
        self.CODIGO += 1

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

    @classe.setter
    def classe(self, classe: Classe):
        if not isinstance(classe, Classe):
            raise TypeError("classe deve ser uma Classe")
        self.__classe = classe

    @property
    def poderes(self):
        return self.__poderes

    @poderes.setter
    def poderes(self, poderes: list[Poder]):
        if any(not isinstance(poder, Poder) for poder in poderes):
            raise TypeError("poderes deve ser uma list[Poder]")

        poderes.sort(key=lambda obj: (-obj.nivel, obj.nome))
        self.__poderes = poderes

    @property
    def vida_atual(self):
        return self.__vida_atual

    @property
    def mana_atual(self):
        return self.__mana_atual

    @property
    def codigo(self):
        return self.__codigo

    def adicionar_poder(self, poder: Poder):
        """
        Adiciona um poder no personagem
        :param poder: Poder que será adicionado
        :return: True
        """
        if not isinstance(poder, Poder):
            raise TypeError("poder deve ser um Poder")

        if any([item.nome for item in self.__poderes]):
            raise DuplicadoException(
                f'Não foi possivel criar o personagem pois ele já possui o mesmo poder {poder.nome}'
            )

        self.__poderes.append(poder)
        return True

    def remover_poder(self, nome: str):
        """Remove um poder do personagem"""
        if not isinstance(nome, str):
            raise TypeError("nome deve ser um uma string")

        for index, poder in enumerate(self.__poderes):
            if poder.nome == nome:
                self.__poderes.pop(index)
                return True
        else:
            return False

    def restaurar_personagem(self):
        """O personagem volta com sua vida e mana inicial"""
        self.__vida_atual = self.classe.vida
        self.__mana_atual = self.classe.mana

    def mudar_vida_atual(self, valor):
        """
        Quando um personagem leva dano ou é curado sua vida muda
        :param valor: Alteração na sua vida
        """
        if not isinstance(valor, int):
            raise TypeError("valor deve ser um um inteiro")

        self.__vida_atual -= valor

        # Vida não pode ser menor do que 0 e não pode ser maior que a vida inicial do personagem
        if self.__vida_atual > self.__classe.vida:
            self.__vida_atual = self.__classe.vida
        elif self.__vida_atual < 0:
            self.__vida_atual = 0

    def gastar_mana(self, valor):
        """Ao utilizar um poder a mana atual do personagem é gasta"""
        if self.__mana_atual - valor < 0:
            raise ValueError("Mana Insuficiente")
        self.__mana_atual -= valor

    @property
    def poderes_disponiveis(self):
        """
        Retorna uma lista com os poderes até certo gasto de mana
        :return: lista de poderes com mana suficiente
        """
        poderes = []
        for poder in self.__poderes:
            if poder.mana_gasta <= self.__mana_atual:
                poderes.append(poder)
        return poderes
