import os
import time

from controllers.controller_classe import ControllerClasse
from controllers.controller_combate import ControllerCombate
from controllers.controller_jogador import ControllerJogador
from controllers.controller_npc import ControllerNpc
from controllers.controller_poder import ControllerPoder
from exceptions.exceptions import CombateAcabouException
from utils.utils import Utils
from views.view_erro import ViewErro
from views.view_menu import ViewMenu


class ControllerMain:

    def __init__(self):
        self.__view_erro = ViewErro()
        self.__view_menu = ViewMenu()
        self.__controller_classe = ControllerClasse()
        self.__controller_poder = ControllerPoder()
        self.__controller_jogador = ControllerJogador(self.__view_erro, self.__controller_classe,
                                                      self.__controller_poder)
        self.__controller_npc = ControllerNpc()
        self.__controller_combate = ControllerCombate(self.__view_erro, self.__controller_jogador,
                                                      self.__controller_npc,
                                                      self.__controller_poder, self.__controller_classe)

    def __criar_classes(self):
        # Gerar classes
        self.__controller_classe.cadastrar_classe("Mago Estudante", 10, 2, 12, 30, 1, "Mago")
        self.__controller_classe.cadastrar_classe("Guerreiro Novato", 30, -2, 16, 10, 1, "Guerreiro")
        self.__controller_classe.cadastrar_classe("Ladino Aprendiz", 15, 5, 15, 15, 1, "Ladino")

        self.__controller_classe.cadastrar_classe("Mago", 20, 2, 12, 40, 2, "Mago")
        self.__controller_classe.cadastrar_classe("Guerreiro", 40, -2, 17, 12, 2, "Guerreiro")
        self.__controller_classe.cadastrar_classe("Ladino", 30, 5, 15, 20, 2, "Ladino")

        self.__controller_classe.cadastrar_classe("Arquimago", 30, 2, 13, 50, 3, "Mago")
        self.__controller_classe.cadastrar_classe("Guerreiro Mestre", 50, -2, 19, 15, 3, "Guerreiro")
        self.__controller_classe.cadastrar_classe("Ladino Chefe", 40, 8, 16, 25, 3, "Ladino")

        self.__controller_classe.cadastrar_classe("Minion", 10, 5, 10, 5, 0)
        self.__controller_classe.cadastrar_classe("Boss", 120, -4, 14, 30, 5)

    def __criar_poderes(self):
        # Gerar poderes
        # Curas, gasto de mana médio,
        self.__controller_poder.cadastrar_poder("Cura Inferior", acerto=10, dano=10, mana_gasta=5, alvos=1,
                                                ataque=False, nivel=1)
        self.__controller_poder.cadastrar_poder("Cura Regular", acerto=10, dano=15, mana_gasta=7, alvos=1, ataque=False,
                                                nivel=2)
        self.__controller_poder.cadastrar_poder("Cura Superior", acerto=10, dano=20, mana_gasta=8, alvos=1,
                                                ataque=False, nivel=3)

        # Sem gasto de mana, porem dano medio e acerto medio
        self.__controller_poder.cadastrar_poder("Espada de Bronze", acerto=7, dano=8, mana_gasta=0, alvos=1,
                                                ataque=True, nivel=1)
        self.__controller_poder.cadastrar_poder("Espada de Aço", acerto=8, dano=10, mana_gasta=0, alvos=1, ataque=True,
                                                nivel=2)
        self.__controller_poder.cadastrar_poder("Espada de Adamantio", acerto=9, dano=12, mana_gasta=0, alvos=1,
                                                ataque=True, nivel=3)

        # Sem gasto de mana, porem dano baixo e acerto alto
        self.__controller_poder.cadastrar_poder("Adaga de Bronze", acerto=9, dano=4, mana_gasta=0, alvos=1, ataque=True,
                                                nivel=1)
        self.__controller_poder.cadastrar_poder("Adaga de Aço", acerto=11, dano=6, mana_gasta=0, alvos=1, ataque=True,
                                                nivel=2)
        self.__controller_poder.cadastrar_poder("Adaga de Adamantio", acerto=13, dano=8, mana_gasta=0, alvos=1,
                                                ataque=True, nivel=3)

        # Ataques em área, gasto de mana medio/alto, porem dano alto e acerto alto
        self.__controller_poder.cadastrar_poder("Ataque Giratório", acerto=5, dano=5, mana_gasta=3, alvos=2,
                                                ataque=True, nivel=1)
        self.__controller_poder.cadastrar_poder("Golpe Poderoso", acerto=4, dano=20, mana_gasta=4, alvos=1, ataque=True,
                                                nivel=1)
        self.__controller_poder.cadastrar_poder("Raio de Fogo", acerto=5, dano=6, mana_gasta=4, alvos=3, ataque=True,
                                                nivel=1)
        self.__controller_poder.cadastrar_poder("Bola de Fogo", acerto=7, dano=10, mana_gasta=10, alvos=3, ataque=True,
                                                nivel=2)
        self.__controller_poder.cadastrar_poder("Golpe Esmagador", acerto=3, dano=20, mana_gasta=10, alvos=2,
                                                ataque=True, nivel=3)
        self.__controller_poder.cadastrar_poder("Lançamento de Pedras", acerto=6, dano=10, mana_gasta=15, alvos=2,
                                                ataque=True, nivel=4)

    def __criar_combates(self):
        # Combate 1
        self.__controller_npc.cadastrar_personagem("Hobgoblin", self.__controller_classe.get_classe("Guerreiro Novato"),
                                                   [self.__controller_poder.get_poder("Espada de Aço"),
                                                    self.__controller_poder.get_poder("Ataque Giratório"),
                                                    self.__controller_poder.get_poder("Golpe Poderoso")]
                                                   )

        self.__controller_npc.cadastrar_personagem("Kobold", self.__controller_classe.get_classe("Ladino Aprendiz"),
                                                   [self.__controller_poder.get_poder("Adaga de Aço")]
                                                   )
        npcs_combate1 = [self.__controller_npc.get_personagem("Kobold"),
                         self.__controller_npc.get_personagem("Hobgoblin")]
        self.__controller_combate.cadastrar_combate(npcs_combate1)

        # Combate 2
        npcs_combate2 = [
            self.__controller_npc.cadastrar_personagem(f"Gnomo{i}", self.__controller_classe.get_classe("Minion"),
                                                       [self.__controller_poder.get_poder("Adaga de Aço"),
                                                        self.__controller_poder.get_poder("Ataque Giratório")]
                                                       ) for i in range(1, 8)]
        self.__controller_combate.cadastrar_combate(npcs_combate2)

        # Combate 3
        npcs_combate3 = [
            self.__controller_npc.cadastrar_personagem(f"Rei Gnomo", self.__controller_classe.get_classe("Boss"),
                                                       [self.__controller_poder.get_poder("Golpe Esmagador"),
                                                        self.__controller_poder.get_poder("Lançamento de Pedras"),
                                                        self.__controller_poder.get_poder("Espada de Adamantio")
                                                        ]
                                                       ),
            self.__controller_npc.get_personagem("Gnomo1"),
            self.__controller_npc.get_personagem("Gnomo2"),
            self.__controller_npc.get_personagem("Gnomo3")]
        self.__controller_combate.cadastrar_combate(npcs_combate3)

    def __criar_personagens(self):
        self.__controller_jogador.cadastrar_personagem("Jorge", self.__controller_classe.get_classe("Mago Estudante"),
                                                       [self.__controller_poder.get_poder("Bola de Fogo"),
                                                        self.__controller_poder.get_poder("Adaga de Bronze"),
                                                        self.__controller_poder.get_poder("Cura Inferior")])
        self.__controller_jogador.cadastrar_personagem("João", self.__controller_classe.get_classe("Guerreiro Novato"),
                                                       [self.__controller_poder.get_poder("Ataque Giratório"),
                                                        self.__controller_poder.get_poder("Espada de Bronze"),
                                                        self.__controller_poder.get_poder("Golpe Poderoso")])
        self.__controller_jogador.cadastrar_personagem("Jaime", self.__controller_classe.get_classe("Ladino Aprendiz"),
                                                       [self.__controller_poder.get_poder("Ataque Giratório"),
                                                        self.__controller_poder.get_poder("Adaga de Bronze"),
                                                        self.__controller_poder.get_poder("Golpe Poderoso")])

    def iniciar(self):
        self.__criar_classes()
        self.__criar_poderes()
        self.__criar_combates()
        # Personagens iniciais caso não queiram criar
        self.__criar_personagens()

        combates_vencidos = 0
        while True:
            try:
                # Display menu
                os.system("cls")
                escolha = self.__view_menu.menu_inicial(combates_vencidos)

                Utils.check_inteiro_intervalo(escolha, [0, combates_vencidos + 3])

                os.system("cls")

                escolha = int(escolha)
                # O grupo será composto por 3 personagens
                if escolha == 0:
                    # Criar grupo de personagens
                    self.__controller_jogador.personagens = []
                    # Grupo possui 3 personagens
                    for index in range(1, 4):
                        self.__controller_jogador.criar_personagem(index, combates_vencidos)
                elif escolha == 1:
                    # Mostrar grupo atual
                    self.__view_menu.grupo(self.__controller_jogador.grupo_estatisticas())
                    time.sleep(5)
                elif 1 < escolha < combates_vencidos + 3:
                    # Iniciar um combate
                    vitoria = self.__controller_combate.iniciar_combate(escolha - 2)
                    time.sleep(5)
                    os.system("cls")

                    # Vencer o ultimo combate liberado faz o personagem aumentar de nivel
                    if vitoria and escolha == combates_vencidos + 2:
                        combates_vencidos += 1
                        self.__controller_jogador.aumentar_nivel()
                else:
                    self.__view_menu.sair()
                    break

            except TypeError:
                self.__view_erro.apenas_inteiros()
                time.sleep(2)
            except CombateAcabouException:
                self.__view_menu.desistir()
                time.sleep(2)
            except Exception:
                self.__view_erro.erro_inexperado_menu()
                time.sleep(2)
