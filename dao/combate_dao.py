from dao.dao import DAO
from dao.jogador_dao import JogadorDAO
from dao.npc_dao import NpcDAO
from exceptions import exceptions
from models.combate import Combate


class CombateDAO(DAO):
    def __init__(self):
        super().__init__('data/combates.pkl')
        self.__jogador_dao = JogadorDAO()
        self.__npc_dao = NpcDAO()

    def add(self, combate: Combate, **kwargs):
        if not isinstance(combate, Combate):
            raise TypeError("combate deve ser um Combate")

        if not isinstance(combate.codigo, int):
            raise TypeError("Key deve ser uma integer")

        try:
            self.get(combate.codigo)
            raise exceptions.DuplicadoException(f"Combate com codigo {combate.codigo} já existe")
        except exceptions.NaoEncontradoException:
            pass

        super().add(combate.codigo, combate)

    def update(self, combate: Combate, **kwargs):
        if not isinstance(combate, Combate):
            raise TypeError("combate deve ser um Combate")

        if not isinstance(combate.codigo, int):
            raise TypeError("Key deve ser uma integer")

        super().update(combate.codigo, combate)

        for jogador in combate.jogadores:
            self.__jogador_dao.update(jogador)

        for npc in combate.npcs:
            self.__npc_dao.update(npc)

    def get(self, key: int):
        if not isinstance(key, int):
            raise TypeError("Key deve ser uma integer")

        return super().get(key)

    def remove(self, key: int):
        """
        Deleta um combate por codigo
        :param key: codigo do combate deletado
        """
        if not isinstance(key, int):
            raise TypeError("Key deve ser uma integer")

        super().remove(key)
