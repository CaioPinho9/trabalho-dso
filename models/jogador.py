from models.personagem import Personagem
from models.classe import Classe


class Jogador(Personagem):
    def __init__(self, nome: str, classe: Classe):

        if not isinstance(nome, str):
            raise TypeError("Nome do jogador deve ser do tipo string")
        if not isinstance(classe, Classe):
            raise TypeError("Classe do jogador deve ser do tipo Classe")

        super().__init__(nome, classe)
        self.__dano_causado = 0
        self.__dano_recebido = 0

    @property
    def dano_causado(self):
        return self.__dano_causado

    @property
    def dano_recebido(self):
        return self.__dano_recebido

    @dano_causado.setter
    def dano_causado(self, valor):
        if not isinstance(valor, int):
            raise TypeError("Dano causado deve ser do tipo inteiro")
        self.__dano_causado = valor

    @dano_recebido.setter
    def dano_recebido(self, valor):
        if not isinstance(valor, int):
            raise TypeError("Dano recebido deve ser do tipo inteiro")
        self.__dano_recebido = valor
