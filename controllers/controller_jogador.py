import os
import random
import time

from controllers.controller_classe import ControllerClasse
from controllers.controller_personagem import ControllerPersonagem
from controllers.controller_poder import ControllerPoder
from exceptions.exceptions import DuplicadoException
from models.jogador import Jogador
from utils.utils import Utils
from views.view_erro import ViewErro
from views.view_jogador import ViewJogador


class ControllerJogador(ControllerPersonagem):
    def __init__(self, view_jogador: ViewJogador,
                 view_erro: ViewErro,
                 controller_classe: ControllerClasse,
                 controller_poder: ControllerPoder):
        super().__init__()
        self.__view_jogador = view_jogador
        self.__view_erro = view_erro
        self.__controller_classe = controller_classe
        self.__controller_poder = controller_poder

    def cadastrar_personagem(self, index_personagem: int, **kwargs):
        while True:
            nome = self.__view_jogador.escolha_nome(index_personagem)

            if not self.get_personagem(nome):
                break

            self.__view_erro.nome_repetido(nome)

        # Escolher a classe do personagem
        while True:
            index = self.__view_jogador.escolha_classe(self.__controller_classe.classe_estatisticas())

            # Impede valores invalidos
            if Utils.check_inteiro_intervalo(index, [0, len(self.__controller_classe.classes) - 1]):
                classe = self.__controller_classe.get_classe_por_index(int(index))
                break
            self.__view_erro.apenas_inteiros()

        jogador = Jogador(nome, classe)
        super().personagens.append(jogador)

        # Mostra todos os poderes iniciais
        poderes_iniciais = self.__controller_poder.poderes_por_nivel(1)
        poderes_estatisticas = self.__controller_poder.poderes_estatisticas(poderes_iniciais)
        self.__view_jogador.aviso_escolher_poderes(nome, poderes_estatisticas)

        # O jogador deve escolher 3 poderes
        quantidade_poderes = 0
        while quantidade_poderes != 3:
            poder = None

            index = self.__view_jogador.escolha_poderes(quantidade_poderes + 1)

            try:
                if Utils.check_inteiro_intervalo(index, [0, len(poderes_iniciais) - 1]):
                    poder = poderes_iniciais[int(index)]
                    super().adicionar_poder_personagem(nome, poder)
                else:
                    self.__view_erro.apenas_inteiros()
            except DuplicadoException:
                self.__view_erro.poder_repetido(nome, poder.nome)

            # Lembrando que todos possuem Soco como poder basico
            quantidade_poderes = len(jogador.poderes) - 1

        poderes_mensagem = self.__controller_poder.poderes_nomes(jogador.poderes)

        os.system("cls")

        self.__view_jogador.aviso_criado(nome, classe.nome, poderes_mensagem, Utils.xingamento())
        time.sleep(3)
        os.system("cls")
