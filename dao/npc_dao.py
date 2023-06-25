from dao.personagem_dao import PersonagemDAO
from models.npc import Npc


class NpcDAO(PersonagemDAO):
    def __init__(self):
        super().__init__('data/npcs.pkl')

    def add(self, npc: Npc, **kwargs):
        if not isinstance(npc, Npc):
            raise TypeError("npc deve ser um Npc")

        super().add(npc)

    def update(self, npc: Npc, **kwargs):
        if not isinstance(npc, Npc):
            raise TypeError("npc deve ser um Npc")

        super().update(npc)
