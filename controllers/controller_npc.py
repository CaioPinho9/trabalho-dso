from controllers.controller_personagem import ControllerPersonagem
from models.classe import Classe
from models.npc import Npc
from models.poder import Poder


class ControllerNpc(ControllerPersonagem):
    def cadastrar_personagem(self, nome: str, classe: Classe):
        super().personagens.append(Npc(nome, classe))
