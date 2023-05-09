from controllers.controller_jogador import ControllerJogador
from controllers.controller_npc import ControllerNpc
from exceptions.exceptions import DuplicadoException, NaoEncontradoException, CombateAcabou
from models.combate import Combate


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

    def _ordernar_batalha(self):
        jogadores = self.__combate_atual.jogadores
        inimigos = self.__combate_atual.inimigos
        ordem_batalha = {}

        for jogador in jogadores:
            resultado_velocidade = self.__controller_jogador.calcular_velocidade(jogador.classe.velocidade)
            ordem_batalha[jogador] = resultado_velocidade

        for inimigo in inimigos:
            resultado_velocidade = self.__controller_npc.calcular_velocidade(inimigo.classe.velocidade)
            ordem_batalha[inimigo] = resultado_velocidade

        # Ordenando pela velocidade
        ordem_batalha = sorted(ordem_batalha.items(), key=lambda x: x[1])
        return [x[0] for x in ordem_batalha]

    def _testar_personagens_vivos(self):
        jogadores = self.__combate_atual.jogadores
        inimigos = self.__combate_atual.inimigos

        if sum(inimigo.vida for inimigo in inimigos) == 0:
            raise CombateAcabou("Combate vencido. Todos os inimigos foram mortos.")

        if sum(jogador.vida for jogador in jogadores) == 0:
            raise CombateAcabou("Game Over. Todos os jogadores perderam a vida.")

    def iniciar_combate(self, codigo: int):
        for index, combate_existente in enumerate(self.__combates):
            if combate_existente.codigo == codigo:
                self.__combate_atual = combate_existente

        if not self.__combate_atual:
            raise NaoEncontradoException("Combate não encontrado")

        self.__combate_atual.ordem_batalha = self._ordernar_batalha()

        try:
            while True:

                self._testar_personagens_vivos()
        except:
            pass


