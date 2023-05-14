from models.personagem import Personagem
from models.classe import Classe
from models.poder import Poder


class Jogador(Personagem):
    def __init__(self, nome: str, classe: Classe, poderes: list[Poder] = []):
        super().__init__(nome, classe, poderes)