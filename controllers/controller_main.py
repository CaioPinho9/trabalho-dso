from controllers.controller_classe import ControllerClasse
from controllers.controller_combate import ControllerCombate
from controllers.controller_jogador import ControllerJogador
from controllers.controller_npc import ControllerNpc
from controllers.controller_poder import ControllerPoder
from exceptions import exceptions
from utils.opcoes_menus import MenuInicial
from utils.setup import setup

from views.view_menu import ViewMenu


class ControllerMain:

    def __init__(self):
        self.__view_menu = ViewMenu()
        self.__controller_classe = ControllerClasse()
        self.__controller_poder = ControllerPoder()
        self.__controller_jogador = ControllerJogador(
            self.__controller_classe,
            self.__controller_poder
        )
        self.__controller_npc = ControllerNpc()
        self.__controller_combate = ControllerCombate(
            self.__controller_jogador,
            self.__controller_npc,
            self.__controller_poder,
            self.__controller_classe
        )

    def recriar_objetos(self, resetar=False):
        inicializado = len(self.__controller_classe.get_all()) == 0
        inicializado |= len(self.__controller_poder.get_all()) == 0
        inicializado |= len(self.__controller_combate.get_all()) == 0
        inicializado |= len(self.__controller_jogador.get_all()) == 0

        if not inicializado and not resetar:
            return

        setup(
            controller_classe=self.__controller_classe,
            controller_poder=self.__controller_poder,
            controller_npc=self.__controller_npc,
            controller_jogador=self.__controller_jogador,
            controller_combate=self.__controller_combate,
        )

    def main(self):
        self.recriar_objetos()
        while True:
            nivel = self.__controller_jogador.get_all()[0].classe.nivel
            try:
                # Display menu
                escolha = self.__view_menu.menu_inicial(nivel)

                # O grupo será composto por 3 personagens
                if escolha == MenuInicial.CRIAR_GRUPO:
                    # Criar grupo de personagens
                    # Grupo possui 3 personagens
                    for index in range(1, 4):
                        self.__controller_jogador.criar_personagem(index, nivel)

                elif escolha == MenuInicial.MOSTRAR_GRUPO:
                    # Mostrar grupo atual
                    estatisticas_classes = []
                    nomes_poderes_personagens = []
                    for jogador in self.__controller_jogador.get_all():
                        estatisticas_classes.append(self.__controller_classe.estatisticas_dict(jogador.classe.nome))
                        nomes_poderes_personagens.append(self.__controller_poder.nomes(jogador.poderes))

                    self.__view_menu.grupo(
                        self.__controller_jogador.nomes(self.__controller_jogador.get_all()),
                        estatisticas_classes,
                        nomes_poderes_personagens,
                        nivel
                    )

                elif escolha == MenuInicial.MOSTRAR_ESTATISTICAS:
                    # Mostrar grupo atual
                    self.__view_menu.estatisticas(
                        self.__controller_jogador.estatisticas(),
                    )

                elif escolha == MenuInicial.RESETAR_DATABASE:
                    # Mostrar grupo atual
                    self.__view_menu.resetar_database()
                    self.recriar_objetos(True)

                elif escolha.value in MenuInicial.COMBATES.value:
                    combate_numero = escolha.value

                    # Iniciar um combate
                    vitoria = self.__controller_combate.iniciar_combate(combate_numero)

                    # Vencer o ultimo combate liberado faz o personagem aumentar de nivel
                    if vitoria and nivel != 3:
                        nivel += 1
                        self.__controller_jogador.aumentar_nivel()
            except exceptions.FecharPrograma as e:
                break
            except exceptions.SairCombate as e:
                pass
            except exceptions.VoltarMenu as e:
                pass
            except Exception as e:
                pass
        self.__view_menu.sair()
