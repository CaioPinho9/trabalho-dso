from models.personagem import Personagem
from models.classe import Classe


class Npc(Personagem):
    def __init__(self, nome: str, classe: Classe, nivel: int):
        super().__init__(nome, classe, nivel)
