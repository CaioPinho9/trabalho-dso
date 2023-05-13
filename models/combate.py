from models.jogador import Jogador
from models.npc import Npc
from models.personagem import Personagem


class Combate:
    def __init__(self, codigo: int, jogadores: list[Jogador], npcs: list[Npc]):
        if not isinstance(codigo, int):
            raise TypeError("Código do combate deve ser do tipo inteiro")
        if not isinstance(jogadores, list):
            raise TypeError("Jogadores do combate deve ser do tipo lista")
        if not isinstance(npcs, list):
            raise TypeError("Npcs do combate deve ser do tipo lista")
        if not all(isinstance(jogador, Jogador) for jogador in jogadores):
            raise TypeError("Jogadores do combate devem ser do tipo Jogador")
        if not all(isinstance(npc, Npc) for npc in npcs):
            raise TypeError("Npcs do combate devem ser do tipo Npc")
        if len(jogadores) == 0:
            raise ValueError("Combate deve ter pelo menos um jogador")
        if len(npcs) == 0:
            raise ValueError("Combate deve ter pelo menos um npc")

        self.__codigo = codigo
        self.__npcs = npcs
        self.__jogadores = jogadores
        self.__ordem_de_batalha = []
        self.__vitoria = 0
        self.__dano_causado = 0
        self.__dano_recebido = 0
        self.__finalizado = False

    @property
    def codigo(self):
        return self.__codigo

    @property
    def jogadores(self):
        return self.__jogadores

    @property
    def npcs(self):
        return self.__npcs

    @property
    def ordem_de_batalha(self):
        return self.__ordem_de_batalha

    @property
    def vitoria(self):
        return self.__vitoria

    @property
    def dano_causado(self):
        return self.__dano_causado

    @property
    def dano_recebido(self):
        return self.__dano_recebido

    @property
    def finalizado(self):
        return self.__finalizado

    @jogadores.setter
    def jogadores(self, lista_de_jogadores):
        if not isinstance(lista_de_jogadores, list):
            raise TypeError("Jogadores deve ser do tipo lista")
        if not all(isinstance(jogador, Jogador) for jogador in lista_de_jogadores):
            raise TypeError("Jogadores deve ser do tipo Jogador")
        if len(lista_de_jogadores) == 0:
            raise ValueError("Combate deve ter pelo menos um jogador")
        self.__jogadores = lista_de_jogadores

    @npcs.setter
    def npcs(self, lista_de_npcs):
        if not isinstance(lista_de_npcs, list):
            raise TypeError("Npcs deve ser do tipo lista")
        if not all(isinstance(npc, Npc) for npc in lista_de_npcs):
            raise TypeError("Npcs deve ser do tipo Npc")
        if len(lista_de_npcs) == 0:
            raise ValueError("Combate deve ter pelo menos um npc")
        self.__npcs = lista_de_npcs

    @ordem_de_batalha.setter
    def ordem_de_batalha(self, lista_de_batalha):
        if not isinstance(lista_de_batalha, list):
            raise TypeError("Ordem de batalha deve ser do tipo lista")
        if not all(isinstance(batalha, Personagem) for batalha in lista_de_batalha):
            raise TypeError("Ordem de batalha deve ser do tipo Personagem")
        self.__ordem_de_batalha = lista_de_batalha

    @vitoria.setter
    def vitoria(self, valor):
        if not isinstance(valor, int):
            raise TypeError("Vitoria deve ser do tipo inteiro")
        self.__vitoria = valor

    @dano_causado.setter
    def dano_causado(self, valor):
        if not isinstance(valor, int):
            raise TypeError("Dano causado deve ser do tipo inteiro")
        self.__dano_causado = valor

    @dano_recebido.setter
    def dano_recebido(self, valor):
        if not isinstance(valor, int):
            raise TypeError("Dano recebido deve ser do tipo inteiro")
        self.__dano_recebido = valor

    @finalizado.setter
    def finalizado(self, valor):
        if not isinstance(valor, bool):
            raise TypeError("Finalizado deve ser do tipo booleano")
        self.__finalizado = valor

    def proximo_da_batalha(self):
        if len(self.__jogadores) <= 0:
            raise ValueError("Não há jogadores para batalhar")
        if len(self.__npcs) <= 0:
            raise ValueError("Não há npcs para batalhar")
        while True:
            proximo_da_batalha = self.__ordem_de_batalha.pop(0)
            self.__ordem_de_batalha.append(proximo_da_batalha)
            # Pula personagens com 0 de vida
            if proximo_da_batalha.vida_atual != 0:
                break

        return proximo_da_batalha
