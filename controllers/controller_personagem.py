from abc import ABC, abstractmethod

from exceptions.exceptions import NaoEncontradoException
from models.classe import Classe
from models.personagem import Personagem
from models.poder import Poder


class ControllerPersonagem(ABC):
    @abstractmethod
    def cadastrar(self, nome: str, classe: Classe, poderes=None):
        pass

    @abstractmethod
    def remover(self, nome: str):
        pass

    @property
    @abstractmethod
    def personagens(self):
        pass

    @personagens.setter
    @abstractmethod
    def personagens(self, personagens):
        pass

    @abstractmethod
    def get_com_nome(self, nome: str):
        """
        Obtém um personagem da lista de personagens.

        Parâmetros:
        nome (str): nome do Personagem a ser encontrado.

        Retorno:
        Personagem: objeto Personagem com o mesmo nome, caso encontrado; ou None, caso não encontrado.
        """
        pass

    @staticmethod
    def vida_mana_estatisticas(personagens: list[Personagem]):
        """
        Retorna uma lista de dicionarios contendo nome, vida e mana atual, vida e mana máxima
        :param personagens: list[Personagem]
        :return:
        list[{"nome": personagem.nome,
             "vida_atual": str(personagem.vida_atual),
             "vida_maxima": str(personagem.classe.vida),
             "mana_atual": str(personagem.mana_atual),
             "mana_maxima": str(personagem.classe.mana)}]
        """
        estatisticas = []
        for personagem in personagens:
            dictionario = {"nome": personagem.nome,
                           "vida_atual": str(personagem.vida_atual), "vida_maxima": str(personagem.classe.vida),
                           "mana_atual": str(personagem.mana_atual), "mana_maxima": str(personagem.classe.mana)}

            estatisticas.append(dictionario)
        return estatisticas

    @abstractmethod
    def restaurar_vida_mana(self):
        """Todos os personagens voltam a ficar com a vida e a mana máxima"""
        pass

    @staticmethod
    def nomes(personagens: list[Personagem]):
        """
        Retorna uma string formatada com os nomes dos personagens
        :param personagens:
        :return: list[personagem.nome]
        """
        if not all(isinstance(personagem, Personagem) for personagem in personagens):
            return TypeError("A lista deve conter personagens")
        return [personagem.nome for personagem in personagens]
