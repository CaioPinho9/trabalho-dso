from models.item import Item
from exceptions.exceptions import DuplicadoException


class ControllerItem:

    def __init__(self):
        self.__itens = []

    def criar_item(self, novo_item: Item):
        if not isinstance(novo_item, Item):
            raise TypeError("item deve ser um objeto da classe Item")

        if self.get_item(novo_item.nome):
            raise DuplicadoException("Já existe um item com esse nome")

        self.__itens.append(novo_item)

        return True

    def remover_item(self, item: Item):
        if not isinstance(item, Item):
            raise TypeError("item deve ser um objeto da classe Item")

        item = self.get_item(item.nome)
        if item:
            self.__itens.remove(item)
            return True
        else:
            return False

    def item(self, nome: str):
        pass

    def get_item(self, nome: str):
        for item in self.__itens:
            if item.nome == nome:
                return item
        return None
