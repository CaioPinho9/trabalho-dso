from models.jogador import Jogador
from models.npc import Npc
from models.personagem import Personagem


class Combate:
    def __init__(self, codigo: int, npcs: list[Npc]):
        if not isinstance(codigo, int):
            raise TypeError("codigo deve ser um inteiro")
        if not isinstance(npcs, list):
            raise TypeError("Npcs do combate deve ser do tipo lista")
        if not all(isinstance(npc, Npc) for npc in npcs):
            raise TypeError("Npcs do combate devem ser do tipo Npc")
        if len(npcs) == 0:
            raise ValueError("Combate deve ter pelo menos um npc")

        self.__codigo = codigo
        self.__npcs = npcs
        self.__jogadores = []
        self.__ordem_de_batalha = []
        self.__contador_turno = 1
        self.__iniciado = False

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
    def personagens(self):
        return [*self.__jogadores, *self.__npcs]

    @property
    def ordem_de_batalha(self):
        return self.__ordem_de_batalha

    @property
    def contador_turno(self):
        return self.__contador_turno

    @property
    def iniciado(self):
        return self.__iniciado

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
        if not all(isinstance(personagem, Personagem) for personagem in lista_de_batalha):
            raise TypeError("Ordem de batalha deve ser do tipo list[Personagem]")
        self.__ordem_de_batalha = lista_de_batalha

    @contador_turno.setter
    def contador_turno(self, contador_turno):
        if not isinstance(contador_turno, int):
            raise TypeError("contador_turno deve ser do tipo int")
        self.__contador_turno = contador_turno

    @iniciado.setter
    def iniciado(self, iniciado):
        if not isinstance(iniciado, bool):
            raise TypeError("iniciado deve ser do tipo bool")
        self.__iniciado = iniciado

    def proximo_da_batalha(self):
        """
        Retorna o primeiro valor da lista e o coloca no final
        :return: Personagem
        """
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
