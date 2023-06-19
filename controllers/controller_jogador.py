import os
import time

from controllers.controller_classe import ControllerClasse
from controllers.controller_personagem import ControllerPersonagem
from controllers.controller_poder import ControllerPoder
from exceptions import exceptions
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
        self.__view_jogador = ViewJogador(controller_classe, controller_poder)
        self.__view_erro = view_erro
        self.__controller_classe = controller_classe
        self.__controller_poder = controller_poder

    def cadastrar(self, nome: str, classe: Classe, poderes: list[Poder] = []):
        """
        Adiciona um Jogador na lista de personagens
        :param nome: identicador do Jogador
        :param classe: Classe possui os atributos principais do personagem
        :param poderes: Habilidades que o Jogador pode utilizar
        :return: o Jogador cadastrado
        """
        poderes.insert(0, self.__controller_poder.get_poder("Soco"))
        jogador = Jogador(nome, classe, poderes)

        if super().get_com_nome(nome):
            raise exceptions.DuplicadoException('Não foi possivel criar o jogador pois ja existe um com o mesmo nome')

        super().personagens.append(jogador)

        if len(super().personagens) > 3:
            super().personagens.pop(0)

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
        poderes = self.__controller_poder.get_poderes_por_nivel(1)

        nomes_classes = self.__controller_classe.nomes(classes)
        nomes_poderes = self.__controller_poder.nomes(poderes)

        jogador = None
        while True:
            # Cadastro
            jogador_dict = self.__view_jogador.criacao_jogador(index_personagem, nomes_classes, nomes_poderes, 3,
                                                               self.get_com_nome)
            nome = jogador_dict["nome"]
            classe_nome = jogador_dict["classe"]
            poderes_nome = jogador_dict["poderes"]

            try:
                classe = self.__controller_classe.get_classe(classe_nome)

                poderes = []

                for poder_nome in poderes_nome:
                    poderes.append(self.__controller_poder.get_poder(poder_nome))

                # Aviso de criaçao do personagem
                self.__view_jogador.aviso_criado(jogador_dict)

                # Salvar
                self.cadastrar(nome, classe, poderes)
                break
            except exceptions.VoltarMenu as e:
                pass

        return True

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
                poderes_mensagem = [poder.nome for poder in jogador.poderes]
                self.__view_jogador.aviso_criado(jogador.nome, jogador.classe.nome, poderes_mensagem,
                                                 Utils.adjetivo(jogador.classe.nivel))
                time.sleep(3)
            os.system("cls")

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

        poderes_estatisticas = self.__controller_poder.estatisticas_dict(poderes_disponiveis)
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
                    raise exceptions.ManaInsuficienteException()

                super().adicionar_poder_personagem(jogador.nome, poder)
                quantidade_poderes += 1
            except exceptions.DuplicadoException:
                self.__view_erro.poder_repetido(jogador.nome, poder.nome)
            except exceptions.ManaInsuficienteException:
                self.__view_erro.mana_insuficiente()
            except TypeError:
                self.__view_erro.apenas_inteiros()
