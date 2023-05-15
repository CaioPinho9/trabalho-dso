import os
import time

from controllers.controller_classe import ControllerClasse
from controllers.controller_personagem import ControllerPersonagem
from controllers.controller_poder import ControllerPoder
from exceptions.exceptions import DuplicadoException, ManaInsuficienteException
from models.classe import Classe
from models.jogador import Jogador
from models.poder import Poder
from utils.utils import Utils
from views.view_erro import ViewErro
from views.view_jogador import ViewJogador


class ControllerJogador(ControllerPersonagem):
    def __init__(self, view_erro: ViewErro,
                 controller_classe: ControllerClasse,
                 controller_poder: ControllerPoder):
        super().__init__()
        self.__view_jogador = ViewJogador()
        self.__view_erro = view_erro
        self.__controller_classe = controller_classe
        self.__controller_poder = controller_poder

    def cadastrar_personagem(self, nome: str, classe: Classe, poderes: list[Poder] = []):
        """
        Adiciona um Jogador na lista de personagens
        :param nome: identicador do Jogador
        :param classe: Classe possui os atributos principais do personagem
        :param poderes: Habilidades que o Jogador pode utilizar
        :return: o Jogador cadastrado
        """
        jogador = Jogador(nome, classe, poderes)

        if super().get_personagem(nome):
            raise DuplicadoException('Não foi possivel criar o jogador pois ja existe um com o mesmo nome')

        super().personagens.append(jogador)

    def criar_personagem(self, index_personagem: int, combates_vencidos: int):
        """
        Apresenta escolhas para a criação de um personagem
        :param index_personagem: Qual personagem está sendo criado
        :param combates_vencidos: De acordo com as vitorias é possivel escolher classes mais altas
        :return: Jogador criado
        """
        # Nivel dos personagens criados = combates_vencidos + 1
        if combates_vencidos > 2:
            combates_vencidos = 2
        classes = self.__controller_classe.get_classes_por_nivel(combates_vencidos + 1)

        # Inicio do cadastro
        while True:
            # Escolher o nome do personagem
            nome = self.__view_jogador.escolha_nome(index_personagem)

            # Se esse personagem não existir pode continuar
            if not self.get_personagem(nome):
                break

            self.__view_erro.nome_repetido(nome)
            time.sleep(2)
            os.system("cls")

        os.system("cls")
        # Escolher a classe do personagem
        while True:
            try:
                index = self.__view_jogador.escolha_classe(nome, self.__controller_classe.classes_estatisticas(classes))

                # Impede valores invalidos
                Utils.check_inteiro_intervalo(index, [0, len(classes) - 1])
                classe = classes[int(index)]
                break
            except TypeError:
                self.__view_erro.apenas_inteiros()
                time.sleep(2)
                os.system("cls")
        os.system("cls")

        # Cria personagem
        jogador = Jogador(nome, classe)
        super().personagens.append(jogador)

        # O jogador deve escolher 3 poderes
        self.__escolher_poder(jogador, 3)

        os.system("cls")

        # Aviso de criaçao do personagem
        poderes_mensagem = self.__controller_poder.poderes_nomes(jogador.poderes)
        self.__view_jogador.aviso_criado(nome, classe.nome, poderes_mensagem, Utils.adjetivo(classe.nivel))

        time.sleep(3)
        os.system("cls")

        return jogador

    def aumentar_nivel(self):
        """
        Ao acabar um combate o jogador troca para uma classe de nivel acima e ganha um poder a mais
        """
        for jogador in super().personagens:
            classe_nova = self.__controller_classe.get_classe_superior(jogador.classe.tipo,
                                                                       jogador.classe.nivel + 1)
            if classe_nova != jogador.classe:
                self.__view_jogador.aviso_aumento_nivel(jogador.nome, jogador.classe.nome, classe_nova.nome)
                jogador.classe = classe_nova
                self.__escolher_poder(jogador, 2, True)

                # Aviso de upar do personagem
                poderes_mensagem = self.__controller_poder.poderes_nomes(jogador.poderes)
                self.__view_jogador.aviso_criado(jogador.nome, jogador.classe.nome, poderes_mensagem,
                                                 Utils.adjetivo(jogador.classe.nivel))
                time.sleep(3)
            os.system("cls")

    def grupo_estatisticas(self):
        """
        Retorna uma string formatada com as classes e nomes dos jogadores
        :return: classe_nome adjetivo jogador_nome, classe_nome adjetivo jogador_nome
        """
        grupo_estatisticas = ""
        for index, jogador in enumerate(super().personagens):
            classe_jogador = Utils.adjetivo(jogador.classe.nivel) + " " + jogador.classe.nome + " " + jogador.nome

            if index == len(super().personagens) - 1:
                grupo_estatisticas += " e pelo "
            elif index != 0:
                grupo_estatisticas += ", pelo "

            grupo_estatisticas += classe_jogador

        return grupo_estatisticas

    def __escolher_poder(self, jogador, quantidade_escolha, aumentar_nivel=False):
        """
        Pede para o jogador escolher um dos poderes disponiveis
        :param jogador: jogador que recebera o poder
        :param quantidade_escolha: Quantos poderes ele pode escolher
        :return:
        """
        # Mostra todos os poderes disponiveis, se for aumentar o nivel mostra apenas os poderes do nivel novo
        if not aumentar_nivel:
            poderes_disponiveis = self.__controller_poder.get_poderes_ate_nivel(jogador.classe.nivel)
        else:
            poderes_disponiveis = self.__controller_poder.get_poderes_por_nivel(jogador.classe.nivel)

        poderes_estatisticas = self.__controller_poder.poderes_estatisticas(poderes_disponiveis)
        self.__view_jogador.aviso_escolher_poderes(jogador.nome, quantidade_escolha, poderes_estatisticas)

        quantidade_poderes = 0
        while quantidade_poderes != quantidade_escolha:
            poder = None

            index = self.__view_jogador.escolha_poderes(quantidade_poderes + 1)

            try:
                Utils.check_inteiro_intervalo(index, [0, len(poderes_disponiveis) - 1])
                poder = poderes_disponiveis[int(index)]

                # Nao pode escolher um poder que não possui mana para usar
                if poder.mana_gasta > jogador.classe.mana:
                    raise ManaInsuficienteException()

                super().adicionar_poder_personagem(jogador.nome, poder)
                quantidade_poderes += 1
            except DuplicadoException:
                self.__view_erro.poder_repetido(jogador.nome, poder.nome)
            except ManaInsuficienteException:
                self.__view_erro.mana_insuficiente()
            except TypeError:
                self.__view_erro.apenas_inteiros()
