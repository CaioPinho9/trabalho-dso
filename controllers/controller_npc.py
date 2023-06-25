from controllers.controller_personagem import ControllerPersonagem
from dao.npc_dao import NpcDAO
from models.classe import Classe
from models.npc import Npc


class ControllerNpc(ControllerPersonagem):

    def __init__(self):
        self.__npc_dao = NpcDAO()

    def cadastrar(self, nome: str, classe: Classe, poderes=None):
        """
        Adiciona um Npc na lista de personagens
        :param nome: identicador do Npc
        :param classe: Classe possui os atributos principais do npc
        :param poderes: Habilidades que o Npc pode utilizar
        :return: o Npc cadastrado
        """
        if poderes is None:
            poderes = []

        npc = Npc(nome, classe, self.__npc_dao.get_next_index(), poderes)

        self.__npc_dao.add(npc)

        return npc

    def get(self, nome: str):
        """
        Encontra um npc pelo nome
        :param nome: nome do npc para encontrar
        :return Npc object
        """
        return self.__npc_dao.get(nome)

    def get_all(self):
        """
        Retorna todos os npcs
        :return: lista de todos os npcs
        """
        return self.__npc_dao.get_all()

    def remover(self, nome: str):
        """
        Deleta um npc por nome
        :param nome: nome do npc deletado
        """
        self.__npc_dao.remove(nome)

    def remover_all(self):
        """
        Remove todos os npcs da lista
        """
        self.__npc_dao.clear_file()
        return True

    def restaurar_vida_mana(self):
        """Todos os npcs voltam a ficar com a vida e a mana máxima"""
        for npc in self.__npc_dao.get_all():
            npc.restaurar_personagem()
            self.__npc_dao.update(npc)
