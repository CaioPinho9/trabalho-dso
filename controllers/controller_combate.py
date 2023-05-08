from controllers.controller_jogador import ControllerJogador


class ControllerCombate:

    def __init__(self, view_combate, controller_jogador: ControllerJogador, controller_npcs):
        self.__combates = []
        self.__controller_jogador = controller_jogador
