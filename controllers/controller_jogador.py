from controllers.controller_personagem import ControllerPersonagem
from models.classe import Classe
from models.jogador import Jogador
from views.view_jogador import ViewJogador
from models.poder import Poder
from models.item import Item
from exceptions.exceptions import DuplicadoException


class ControllerJogador(ControllerPersonagem):
    def __init__(self):
        super().__init__()
        self.__tela_jogador = ViewJogador(self)

    def cadastrar_personagem(self, nome: str, classe: Classe, nivel: int):
        self.__tela_jogador.cadastro_jogador()
        super().personagens.append(Jogador(nome, classe, nivel))

    def calcular_ataque(self, poder: Poder):
        if not isinstance(poder, Poder):
            raise TypeError("poder deve ser um objeto da classe Poder")

        return poder.dano

    def calcular_buff(self, item: Item):
        if not isinstance(item, Item):
            raise TypeError("item deve ser um objeto da classe Item")

        return item.buff_ataque

    def remover_item(self, item: Item):
        if not isinstance(item, Item):
            raise TypeError("item deve ser um objeto da classe Item")

        if self.get_item(item.nome):
            raise DuplicadoException("Já existe um item com esse nome")

        self.__itens.append(item)

        return True

    def adicionar_item(self, item: Item):
        if not isinstance(item, Item):
            raise TypeError("item deve ser um objeto da classe Item")

        item = self.get_item(item.nome)
        if item:
            self.__itens.remove(item)

            return True
        else:
            return False

    def remover_personagem(self, nome: str):
        return super().remover_personagem(nome)

    def get_item(self, nome: str):
        for item in self.__itens:
            if item.nome == nome:
                return item
        return None