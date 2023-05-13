from controllers.controller_personagem import ControllerPersonagem
from models.classe import Classe
from models.npc import Npc
from models.poder import Poder


class ControllerNpc(ControllerPersonagem):
    def cadastrar_personagem(self, nome: str, classe: Classe = None):
        if not isinstance(nome, str):
            raise TypeError("nome deve ser uma string")
        if not isinstance(classe, Classe):
            raise TypeError("classe deve ser uma Classe")

        super().personagens.append(Npc(nome, classe))
