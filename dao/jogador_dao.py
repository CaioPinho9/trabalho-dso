from dao.personagem_dao import PersonagemDAO


class JogadorDAO(PersonagemDAO):
    def __init__(self):
        super().__init__('data/jogadores.pkl')
