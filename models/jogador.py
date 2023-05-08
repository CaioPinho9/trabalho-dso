from personagem import Personagem
from item import Item
class Jogador(Personagem):
    def __init__(self, nome, classe, nivel, poderes):

        if not isinstance(nome, str):
            raise TypeError("Nome do jogador deve ser do tipo string")

        super().__init__(nome, classe, nivel, poderes)
        self.__dano_causado = 0
        self.__dano_recebido = 0
        self.__itens = []

        @property
        def dano_causado(self):
            return self.__dano_causado
        
        @property
        def dano_recebido(self):
            return self.__dano_recebido
        
        @property
        def itens(self):
            return self.__itens
        
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
        
        def adicionar_item(self, item):
            if not isinstance(item, Item):
                raise TypeError("Item deve ser do tipo Item")
            self.__itens.append(item)
        
        def remover_item(self, item):
            if not isinstance(item, Item):
                raise TypeError("Item deve ser do tipo Item")
            self.__itens.remove(item)
