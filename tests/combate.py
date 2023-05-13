from controllers.controller_classe import ControllerClasse
from controllers.controller_combate import ControllerCombate
from controllers.controller_jogador import ControllerJogador
from controllers.controller_npc import ControllerNpc
from models.combate import Combate
from models.poder import Poder
from tests.default_models_to_test import CLASSE, PODER
from views.view_combate import ViewCombate
from views.view_jogador import ViewJogador

controller_classe = ControllerClasse()
controller_jogador = ControllerJogador(ViewJogador(), controller_classe)
controller_npc = ControllerNpc()
controller_combate = ControllerCombate(ViewCombate(), controller_jogador, controller_npc)

controller_jogador.cadastrar_personagem("Jogador1")
controller_jogador.adicionar_poder_personagem("Jogador1", PODER)
controller_jogador.adicionar_poder_personagem("Jogador1", Poder("Fireball", 5, 4, 5, 3, True))
controller_jogador.cadastrar_personagem("Jogador2")
controller_jogador.adicionar_poder_personagem("Jogador2", PODER)
controller_jogador.adicionar_poder_personagem("Jogador2", Poder("Heal", 5, 4, 3, 1, False))
controller_npc.cadastrar_personagem("Npc1", CLASSE)
controller_npc.cadastrar_personagem("Npc2", CLASSE)
controller_npc.adicionar_poder_personagem("Npc1", PODER)
controller_npc.adicionar_poder_personagem("Npc2", PODER)


combate = Combate(1, controller_jogador.personagens, controller_npc.personagens)

controller_combate.cadastrar_combate(combate)

controller_combate.iniciar_combate(1)

