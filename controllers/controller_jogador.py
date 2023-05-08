from controllers.controller_personagem import ControllerPersonagem
from models.classe import Classe
from models.jogador import Jogador


class ControllerJogador(ControllerPersonagem):
    def cadastrar_personagem(self, nome: str, classe: Classe, nivel: int):
        super().personagens.append(Jogador(nome, classe, nivel))


