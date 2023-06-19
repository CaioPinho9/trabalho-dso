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
            jogador_dict = self.__view_jogador.criacao_jogador(index_personagem, nomes_classes, nomes_poderes,
                                                               self.get_com_nome, 3 * (combates_vencidos + 1))
            nome = jogador_dict["nome"]
            classe_nome = jogador_dict["classe"]
            poderes_nome = jogador_dict["poderes"]

            classe = self.__controller_classe.get_classe(classe_nome)

            poderes = []

            for poder_nome in poderes_nome:
                poderes.append(self.__controller_poder.get_poder(poder_nome))

            # Salvar
            self.cadastrar(nome, classe, poderes)
            break

        return True

    def aumentar_nivel(self):
        """
        Ao acabar um combate o jogador troca para uma classe de nivel acima e ganha um poder a mais
        """
        for jogador in super().personagens:
            # Encontra a nova classe do personagem
            classe_antiga = jogador.classe
            jogador.classe = self.__controller_classe.get_classe_superior(jogador.classe.tipo, jogador.classe.nivel + 1)

            # Poderes novos que podem ser escolhidos
            poderes_disponiveis = self.__controller_poder.get_poderes_ate_nivel(jogador.classe.nivel)
            poderes_disponiveis = [poder for poder in poderes_disponiveis if poder not in jogador.poderes]
            nomes_poderes = self.__controller_poder.nomes(poderes_disponiveis)

            # Poderes que o personagem já possui
            nomes_poderes_antigos = self.__controller_poder.nomes(jogador.poderes)

            # Soco é um poder obrigatório
            nomes_poderes_antigos.remove("Soco")

            # Atributos da classe nova
            estatisticas_classes_nova = self.__controller_classe.estatisticas_dict(jogador.classe)

            # Tela mostra que passou de nivel e escolhe os poderes
            poderes_escolhidos = self.__view_jogador.aumentar_nivel(jogador.nome,
                                                                    classe_antiga.nome,
                                                                    estatisticas_classes_nova,
                                                                    nomes_poderes,
                                                                    nomes_poderes_antigos)

            # Soco é obrigatório e encontra os poderes pelo nome
            poderes_novos = [self.__controller_poder.get_poder("Soco")]
            for nome in poderes_escolhidos:
                poderes_novos.append(self.__controller_poder.get_poder(nome))

            # Atualiza os poderes
            jogador.poderes = poderes_novos

        # Restaura a vida e mana ao maximo, pois o maximo aumentou
        self.restaurar_vida_mana()

        return True
