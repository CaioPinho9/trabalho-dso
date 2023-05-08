from controllers.controller_personagem import ControllerPersonagem
from models.classe import Classe
from models.npc import Npc


class ControllerNpc(ControllerPersonagem):
    def cadastrar_personagem(self, nome: str, classe: Classe, nivel: int):
        super().personagens.append(Npc(nome, classe, nivel))
