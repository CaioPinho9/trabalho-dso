import os
import random
import time

from controllers.controller_classe import ControllerClasse
from controllers.controller_personagem import ControllerPersonagem
from controllers.controller_poder import ControllerPoder
from dao.jogador_dao import JogadorDAO
from exceptions import exceptions
from models.classe import Classe
from models.jogador import Jogador
from models.poder import Poder
from utils.utils import Utils
from views.view_jogador import ViewJogador


class ControllerJogador(ControllerPersonagem):
    def __init__(self,
                 controller_classe: ControllerClasse,
                 controller_poder: ControllerPoder):
        super().__init__()
        self.__view_jogador = ViewJogador(controller_classe, controller_poder)
        self.__controller_classe = controller_classe
        self.__controller_poder = controller_poder
        self.__jogador_dao = JogadorDAO()

    def cadastrar(self, nome: str, classe: Classe, poderes=None):
        """
        Adiciona um Jogador na lista de personagens
        :param nome: identicador do Jogador
        :param classe: Classe possui os atributos principais do personagem
        :param poderes: Habilidades que o Jogador pode utilizar
        :return: o Jogador cadastrado
        """
        if poderes is None:
            poderes = []
        poderes.insert(0, self.__controller_poder.get_poder("Soco"))
        jogador = Jogador(nome, classe, self.__jogador_dao.get_next_index(), poderes)

        self.__jogador_dao.add(jogador)

        jogadores = self.__jogador_dao.get_all()

        if len(jogadores) > 3:
            primeiro_criado = jogadores[0]
            for jogador in jogadores:
                if jogador.codigo < primeiro_criado.codigo:
                    primeiro_criado = jogador

            self.remover(primeiro_criado.nome)

    def criar_personagem(self, index_personagem: int, nivel: int):
        """
        Apresenta escolhas para a criação de um personagem
        :param index_personagem: Qual personagem está sendo criado
        :param nivel: Nivel dos personagens criados
        :return: Jogador criado
        """
        if nivel > 3:
            nivel = 3
        classes = self.__controller_classe.get_classes_por_nivel(nivel)
        poderes = self.__controller_poder.get_poderes_ate_nivel(nivel)

        poderes.sort(key=lambda obj: (-obj.nivel, obj.nome))

        nomes_classes = self.__controller_classe.nomes(classes)
        nomes_poderes = self.__controller_poder.nomes(poderes)

        jogador = None
        while True:
            # Cadastro
            jogador_dict = self.__view_jogador.criacao_jogador(index_personagem, nomes_classes, nomes_poderes,
                                                               self.get_personagem, 3 + (2 * (nivel - 1)))
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
        for jogador in self.__jogador_dao.get_all():
            # Encontra a nova classe do personagem
            classe_antiga = jogador.classe
            jogador.classe = self.__controller_classe.get_classe_superior(jogador.classe.tipo, jogador.classe.nivel + 1)

            # Poderes novos que podem ser escolhidos
            poderes_disponiveis = self.__controller_poder.get_poderes_ate_nivel(jogador.classe.nivel)
            poderes_disponiveis = [
                poder for poder in poderes_disponiveis
                if poder.nome not in self.__controller_poder.nomes(jogador.poderes)
            ]
            poderes_disponiveis.sort(key=lambda obj: (-obj.nivel, obj.nome))
            nomes_poderes = self.__controller_poder.nomes(poderes_disponiveis)

            # Poderes que o personagem já possui
            nomes_poderes_antigos = self.__controller_poder.nomes(jogador.poderes)

            # Soco é um poder obrigatório
            nomes_poderes_antigos.remove("Soco")

            # Tela mostra que passou de nivel e escolhe os poderes
            poderes_escolhidos = self.__view_jogador.aumentar_nivel(jogador.nome,
                                                                    classe_antiga.nome,
                                                                    jogador.classe.nome,
                                                                    nomes_poderes,
                                                                    nomes_poderes_antigos)

            # Soco é obrigatório e encontra os poderes pelo nome
            poderes_novos = [self.__controller_poder.get_poder("Soco")]
            for nome in poderes_escolhidos:
                poderes_novos.append(self.__controller_poder.get_poder(nome))

            # Atualiza os poderes
            jogador.poderes = poderes_novos
            self.__jogador_dao.update(jogador)

        # Restaura a vida e mana ao maximo, pois o maximo aumentou
        self.restaurar_vida_mana()

        return True

    def restaurar_vida_mana(self):
        """Todos os jogadores voltam a ficar com a vida e a mana máxima"""
        for jogador in self.__jogador_dao.get_all():
            jogador.restaurar_personagem()
            self.__jogador_dao.update(jogador)

    def get_personagem(self, nome: str):
        """
        Encontra um jogador pelo nome
        :param nome: nome do jogador para encontrar
        :return Jogador object
        """
        return self.__jogador_dao.get(nome)

    @property
    def personagens(self):
        """
        Retorna todos os jogadores
        :return: lista de todos os jogadores
        """
        return self.__jogador_dao.get_all()

    @personagens.setter
    def personagens(self, jogadores):
        """
        Atualiza todos os jogadores
        :param jogadores: Lista dos jogadores que serão inseridos
        """
        if not all(isinstance(jogador, Jogador) for jogador in jogadores):
            raise TypeError("jogadores deve ser do tipo list[Jogador]")

        for jogador in self.__jogador_dao.get_all():
            self.__jogador_dao.remove(jogador.nome)

        for jogador in jogadores:
            self.__jogador_dao.add(jogador)

    def remover(self, nome: str):
        """
        Deleta um jogador por nome
        :param nome: nome do jogador deletado
        """

        if not isinstance(nome, str):
            raise TypeError("nome deve ser um uma string")

        self.__jogador_dao.remove(nome)

    def estatisticas(self):
        """
        Retorna uma lista de dicionário com as estatisticas de dano e cura causados, além de recebidos
        :return: lista de dicionários
        """
        estatisticas = []

        for jogador in self.__jogador_dao.get_all():
            estatisticas.append(jogador.estatisticas)

        return estatisticas

    def remover_all(self):
        self.__jogador_dao.clear_file()
