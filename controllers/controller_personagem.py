import random
from abc import ABC, abstractmethod

from controllers.controller_poder import ControllerPoder
from exceptions.exceptions import NaoEncontradoException
from models.classe import Classe
from models.poder import Poder


class ControllerPersonagem(ABC):
    def __init__(self):
        self.__personagens = []

    @abstractmethod
    def cadastrar_personagem(self, nome: str, classe: Classe = None):
        pass

    def remover_personagem(self, nome: str):
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

    def personagens_vivos(self):
        return [personagem for personagem in self.__personagens if personagem.vida_atual > 0]

    @staticmethod
    def calcular_acerto(poder):
        if not isinstance(poder, Poder):
            raise TypeError("ataque deve ser um Poder")

        rolagem_jogador = random.randint(1, 20)
        resultado_acerto = rolagem_jogador + poder.acerto

        return resultado_acerto

    @staticmethod
    def calcular_velocidade(velocidade: int):
        if not isinstance(velocidade, int):
            raise TypeError("velocidade deve ser um inteiro")

        rolagem_jogador = random.randint(1, 20)
        resultado_velocidade = rolagem_jogador + velocidade

        return resultado_velocidade

    @staticmethod
    def personagens_vida_estatisticas_com_index(personagens=None):
        estatisticas = [personagem.nome + "[" + str(index) + "]: " +
                        str(personagem.vida_atual) + "/" + str(personagem.classe.vida) for
                        index, personagem in enumerate(personagens)]
        return "\n".join(estatisticas)

    @staticmethod
    def personagens_vida_mana_estatisticas(personagens=None):
        estatisticas = [personagem.nome + ": HP[" + str(personagem.vida_atual) + "/" +
                        str(personagem.classe.vida) + "] Mana[" + str(personagem.mana_atual) + "/" +
                        str(personagem.classe.mana) + "]" for personagem in personagens]
        return "\n".join(estatisticas)

    @staticmethod
    def personagens_nomes(personagens):
        nomes = [personagem.nome for personagem in personagens]
        return ", ".join(nomes)

    def restaurar_personagens(self):
        for personagem in self.__personagens:
            personagem.restaurar_vida_atual()
            personagem.restaurar_mana_atual()
