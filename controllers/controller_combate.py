from controllers.controller_jogador import ControllerJogador
from controllers.controller_npc import ControllerNpc
from controllers.controller_personagem import ControllerPersonagem
from exceptions.exceptions import DuplicadoException, NaoEncontradoException
from models.combate import Combate
from models.jogador import Jogador
from models.personagem import Personagem


class ControllerCombate:

    def __init__(self, view_combate, controller_jogador: ControllerJogador, controller_npc: ControllerNpc):
        self.__combates = []
        self.__view_combate = view_combate
        self.__controller_jogador = controller_jogador
        self.__controller_npc = controller_npc
        self.__combate_atual: Combate = None

    def cadastrar_combate(self, combate: Combate):
        for index, combate_existente in enumerate(self.__combates):
            if combate_existente.codigo == combate.codigo:
                raise DuplicadoException("Esse combate já existe")

        self.__combates.append(combate)

    def iniciar_combate(self, codigo: int):
        for index, combate_existente in enumerate(self.__combates):
            if combate_existente.codigo == codigo:
                self.__combate_atual = combate_existente

        if not self.__combate_atual:
            raise NaoEncontradoException("Combate não encontrado")

        self.__combate_atual.ordem_batalha = self._ordernar_batalha()

        continuar = True
        while continuar:
            proximo_personagem = self.__combate_atual.proximo_da_batalha()

            self._turno(proximo_personagem)

            continuar, vitoria = self._testar_personagens_vivos()

    def _turno(self, personagem: Personagem):
        if isinstance(personagem, Jogador):
            dano, resultado_acerto, alvos = self.__controller_jogador.turno(personagem, self.__combate_atual.npcs)
        else:
            dano, resultado_acerto, alvos = self.__controller_npc.turno(personagem, self.__combate_atual.jogadores)

    def _ordernar_batalha(self):
        jogadores = self.__combate_atual.jogadores
        npcs = self.__combate_atual.npcs
        ordem_batalha = {}

        for jogador in jogadores:
            resultado_velocidade = ControllerPersonagem.calcular_velocidade(jogador.classe.velocidade)
            ordem_batalha[jogador] = resultado_velocidade

        for npc in npcs:
            resultado_velocidade = ControllerPersonagem.calcular_velocidade(npc.classe.velocidade)
            ordem_batalha[npc] = resultado_velocidade

        # Ordenando pela velocidade
        ordem_batalha = sorted(ordem_batalha.items(), key=lambda x: x[1])
        return [x[0] for x in ordem_batalha]

    def _testar_personagens_vivos(self):
        jogadores = self.__combate_atual.jogadores
        npcs = self.__combate_atual.npcs

        # return Continuar, Vitoria,
        if sum(npc.vida for npc in npcs) == 0:
            return False, False

        if sum(jogador.vida for jogador in jogadores) == 0:
            return False, True

        return True, False
