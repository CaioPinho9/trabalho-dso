import random
from abc import ABC, abstractmethod

from models.classe import Classe
from models.poder import Poder


class ControllerPersonagem(ABC):
    def __init__(self):
        self.__personagens = []

    @abstractmethod
    def cadastrar_personagem(self, nome: str, classe: Classe, nivel: int):
        pass

    def remover_personagem(self, nome: str):
        if not isinstance(nome, str):
            raise TypeError("nome deve ser um uma string")

        for index, personagem in enumerate(self.__personagens):
            if personagem.nome == nome:
                self.__personagens.pop(index)
                return True
        else:
            return False

    def adicionar_poder_personagem(self, nome_personagem: str, poder: Poder):
        if not isinstance(nome_personagem, str):
            raise TypeError("nome deve ser um uma string")

        for index, personagem in enumerate(self.__personagens):
            if personagem.nome == nome_personagem:
                self.__personagens[index].adicionar_poder(poder)
                return True
        else:
            return False

    def remover_poder_personagem(self, nome_personagem: str, nome_poder: str):
        if not isinstance(nome_personagem, str):
            raise TypeError("nome deve ser um uma string")

        for index, personagem in enumerate(self.__personagens):
            if personagem.nome == nome_personagem:
                self.__personagens[index].remover_poder(nome_poder)
                return True
        else:
            return False

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

    @staticmethod
    def calcular_poder(poder):
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

    @staticmethod
    def calcular_velocidade(velocidade: int):
        if not isinstance(velocidade, int):
            raise TypeError("velocidade deve ser um inteiro")

        rolagem_jogador = random.randint(1, 20)
        resultado_velocidade = rolagem_jogador + velocidade

        return resultado_velocidade
