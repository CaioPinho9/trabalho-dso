from controllers.controller_jogador import ControllerJogador


class ViewJogador:

    def __init__(self, controlador: ControllerJogador):
        if not isinstance(controlador, ControllerJogador):
            raise TypeError("controlador deve ser um objeto da classe ControllerJogador")

        self.__controlador = controlador

    def cadastro_jogador():
        pass
