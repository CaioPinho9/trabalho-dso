import random

from controllers.controller_jogador import ControllerJogador
from controllers.controller_personagem import ControllerPersonagem
from models.classe import Classe
from models.npc import Npc
from models.personagem import Personagem
from models.poder import Poder


class ControllerNpc(ControllerPersonagem):
    def cadastrar_personagem(self, nome: str, classe: Classe, nivel: int):
        super().personagens.append(Npc(nome, classe, nivel))

    def turno(self, personagem: Npc, controller_jogador: ControllerJogador):
        poder_aleatorio: Poder = random.choice(personagem.poderes)

        dano, resultado_acerto = ControllerPersonagem.calcular_poder(poder_aleatorio)

        if poder_aleatorio.ataque_cura:
            personagens_alvos = self._escolher_alvo(poder_aleatorio, controller_jogador.personagens_vivos())
        else:
            personagens_alvos = self._escolher_alvo(poder_aleatorio, super().personagens_vivos())
            dano *= 1

        for personagem in personagens_alvos:
            # Todo: change vida atual
            personagem.vida_atual(dano)

        return dano, resultado_acerto, personagens_alvos

    def _escolher_alvo(self, poder_aleatorio: Poder, personagens_vivos: list[Personagem]):
        personagens_alvos = []
        for _ in range(poder_aleatorio.alvos):
            # Selecionando um inimigo aleatório que ainda não foi selecionado
            personagens_disponiveis = list(set(personagens_vivos) - set(personagens_alvos))
            if not personagens_disponiveis:
                break
            personagem_alvo = random.choice(personagens_disponiveis)
            personagens_alvos.append(personagem_alvo)

        return personagens_alvos
