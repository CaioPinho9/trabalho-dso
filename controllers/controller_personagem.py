from abc import ABC, abstractmethod

from exceptions.exceptions import NaoEncontradoException
from models.classe import Classe
from models.personagem import Personagem
from models.poder import Poder


class ControllerPersonagem(ABC):
    def __init__(self):
        self.__personagens = []

    @abstractmethod
    def cadastrar(self, nome: str, classe: Classe, poderes: list[Poder] = []):
        pass

    def remover_by_name(self, nome: str):
        if not isinstance(nome, str):
            raise TypeError("nome deve ser um uma string")

        for index, personagem in enumerate(self.__personagens):
            if personagem.nome == nome:
                self.__personagens.pop(index)
                return True
        raise NaoEncontradoException()

    def adicionar_poder_personagem(self, nome_personagem: str, poder: Poder):
        if not isinstance(nome_personagem, str):
            raise TypeError("nome deve ser um uma string")

        for index, personagem in enumerate(self.__personagens):
            if personagem.nome == nome_personagem:
                self.__personagens[index].adicionar_poder(poder)
                return True
        raise NaoEncontradoException()

    def remover_poder_personagem(self, nome_personagem: str, nome_poder: str):
        if not isinstance(nome_personagem, str):
            raise TypeError("nome deve ser um uma string")

        for index, personagem in enumerate(self.__personagens):
            if personagem.nome == nome_personagem:
                self.__personagens[index].remover_poder(nome_poder)
                return True
        raise NaoEncontradoException()

    @property
    def personagens(self):
        return self.__personagens

    @personagens.setter
    def personagens(self, personagens):
        if not all(isinstance(personagem, Personagem) for personagem in personagens):
            raise TypeError("personagens deve ser do tipo list[Personagem]")
        self.__personagens = personagens

    def get_by_name(self, nome: str):
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

    def vida_estatisticas_com_index(self, personagens: list[Personagem]):
        """
        Retorna uma string formatada com a vida atual e original de uma lista de personagens
        :param personagens: list[Personagem]
        :return:
        nome[index]: [vida_atual/vida]
        nome[index + 1]: [vida_atual/vida]
        """
        estatisticas = [personagem.nome + "[" + str(index) + "]: " +
                        str(personagem.vida_atual) + "/" + str(personagem.classe.vida) for
                        index, personagem in enumerate(personagens)]
        return "\n".join(estatisticas)

    def vida_mana_estatisticas(self, personagens: list[Personagem]):
        """
        Retorna uma string formatada com a vida atual e original de uma lista de personagens
        :param personagens: list[Personagem]
        :return:
        nome: HP[vida_atual/vida] Mana[mana_atual/mana]
        nome: HP[vida_atual/vida] Mana[mana_atual/mana]
        """
        estatisticas = [personagem.nome + ": HP[" + str(personagem.vida_atual) + "/" +
                        str(personagem.classe.vida) + "] Mana[" + str(personagem.mana_atual) + "/" +
                        str(personagem.classe.mana) + "]" for personagem in personagens]
        return "\n".join(estatisticas)

    def restaurar_vida_mana(self):
        """Todos os personagens voltam a ficar com a vida e a mana máxima"""
        for personagem in self.__personagens:
            personagem.restaurar_personagem()

    def nomes(self, personagens: list[Personagem]):
        """
        Retorna uma string formatada com os nomes dos personagens
        :param personagens:
        :return: list[personagem.nome]
        """
        if not all(isinstance(personagem, Personagem) for personagem in personagens):
            return TypeError("A lista deve conter personagens")
        return [personagem.nome for personagem in personagens]
