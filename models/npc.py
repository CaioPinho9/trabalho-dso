from models.personagem import Personagem
from models.classe import Classe
from models.poder import Poder


class Npc(Personagem):
    def __init__(self, nome: str, classe: Classe, codigo: int, poderes=None):
        super().__init__(nome, classe, codigo, poderes)
