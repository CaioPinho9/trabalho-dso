from dao.personagem_dao import PersonagemDAO
from models.jogador import Jogador


class JogadorDAO(PersonagemDAO):
    def __init__(self):
        super().__init__('data/jogadores.pkl')

    def add(self, jogador: Jogador, **kwargs):
        if not isinstance(jogador, Jogador):
            raise TypeError("jogador deve ser um Jogador")

        super().add(jogador)

    def update(self, jogador: Jogador, **kwargs):
        if not isinstance(jogador, Jogador):
            raise TypeError("jogador deve ser um Jogador")

        super().update(jogador)