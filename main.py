import os
import time

from controllers.controller_classe import ControllerClasse
from controllers.controller_combate import ControllerCombate
from controllers.controller_jogador import ControllerJogador
from controllers.controller_npc import ControllerNpc
from controllers.controller_poder import ControllerPoder
from views.view_combate import ViewCombate
from views.view_erro import ViewErro
from views.view_jogador import ViewJogador

view_combate = ViewCombate()
view_jogador = ViewJogador()
view_erro = ViewErro()
controller_classe = ControllerClasse()
controller_poder = ControllerPoder()
controller_jogador = ControllerJogador(view_jogador, view_erro, controller_classe, controller_poder)
controller_npc = ControllerNpc()
controller_combate = ControllerCombate(view_combate, view_erro, controller_jogador, controller_npc,
                                       controller_poder, controller_classe)

# Gerar classes
controller_classe.cadastrar_classe("Mago", 10, 2, 12, 30)
controller_classe.cadastrar_classe("Guerreiro", 30, -2, 18, 10)
controller_classe.cadastrar_classe("Ladino", 15, 5, 15, 15)

# Gerar poderes
# Curas, gasto de mana médio,
controller_poder.cadastrar_poder("Cura Inferior", acerto=10, dano=10, mana_gasta=5, alvos=1, ataque=False, nivel=1)
controller_poder.cadastrar_poder("Cura Regular", acerto=10, dano=15, mana_gasta=7, alvos=1, ataque=False, nivel=2)
controller_poder.cadastrar_poder("Cura Superior", acerto=10, dano=20, mana_gasta=8, alvos=1, ataque=False, nivel=3)

# Sem gasto de mana, porem dano medio e acerto medio
controller_poder.cadastrar_poder("Espada de Bronze", acerto=6, dano=5, mana_gasta=0, alvos=1, ataque=True, nivel=1)
controller_poder.cadastrar_poder("Espada de Aço", acerto=7, dano=8, mana_gasta=0, alvos=1, ataque=True, nivel=2)
controller_poder.cadastrar_poder("Espada de Adamantio", acerto=8, dano=10, mana_gasta=0, alvos=1, ataque=True, nivel=3)

# Sem gasto de mana, porem dano baixo e acerto alto
controller_poder.cadastrar_poder("Adaga de Bronze", acerto=8, dano=3, mana_gasta=0, alvos=1, ataque=True, nivel=1)
controller_poder.cadastrar_poder("Adaga de Aço", acerto=10, dano=5, mana_gasta=0, alvos=1, ataque=True, nivel=2)
controller_poder.cadastrar_poder("Adaga de Adamantio", acerto=12, dano=7, mana_gasta=0, alvos=1, ataque=True, nivel=3)

# Ataques em área, gasto de mana medio/alto, porem dano alto e acerto alto
controller_poder.cadastrar_poder("Ataque Giratório", acerto=4, dano=3, mana_gasta=3, alvos=2, ataque=True, nivel=1)
controller_poder.cadastrar_poder("Bola de Fogo", acerto=6, dano=15, mana_gasta=10, alvos=3, ataque=True, nivel=1)
controller_poder.cadastrar_poder("Golpe Poderoso", acerto=2, dano=15, mana_gasta=4, alvos=1, ataque=True, nivel=1)

# Criar Npcs
controller_npc.cadastrar_personagem("Hobgoblin", controller_classe.get_classe("Guerreiro"))
controller_npc.adicionar_poder_personagem("Hobgoblin", controller_poder.get_poder("Espada de Aço"))
controller_npc.adicionar_poder_personagem("Hobgoblin", controller_poder.get_poder("Ataque Giratório"))
controller_npc.adicionar_poder_personagem("Hobgoblin", controller_poder.get_poder("Golpe Poderoso"))

controller_npc.cadastrar_personagem("Kobold", controller_classe.get_classe("Ladino"))
controller_npc.adicionar_poder_personagem("Kobold", controller_poder.get_poder("Adaga de Aço"))
controller_npc.adicionar_poder_personagem("Kobold", controller_poder.get_poder("Adaga de Bronze"))
controller_npc.adicionar_poder_personagem("Kobold", controller_poder.get_poder("Cura Inferior"))

# Aviso Inicial
os.system("cls")
view_jogador.aviso_iniciar()
time.sleep(7)
os.system("cls")

# O grupo será composto por 3 personagens
for index in range(1, 4):
    controller_jogador.cadastrar_personagem(index)

controller_combate.cadastrar_combate(controller_jogador.personagens, controller_npc.personagens)
controller_combate.iniciar_combate(0)
