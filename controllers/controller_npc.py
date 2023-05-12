from controllers.controller_personagem import ControllerPersonagem
from models.classe import Classe
from models.npc import Npc
from models.poder import Poder


class ControllerNpc(ControllerPersonagem):
    def cadastrar_personagem(self, nome: str, classe: Classe, nivel: int):
        super().personagens.append(Npc(nome, classe, nivel))

    def calcular_ataque(self, poder: Poder):
        if not isinstance(poder, Poder):
            raise TypeError("poder deve ser um objeto da classe Poder")

        return poder.dano
