from dao.personagem_dao import PersonagemDAO


class NpcDAO(PersonagemDAO):
    def __init__(self):
        super().__init__('data/npcs.pkl')
