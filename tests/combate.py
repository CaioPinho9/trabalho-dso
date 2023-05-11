from controllers.controller_combate import ControllerCombate
from controllers.controller_jogador import ControllerJogador
from controllers.controller_npc import ControllerNpc
from models.combate import Combate
from tests.default_models_to_test import CLASSE, PODER
from views.view_combate import ViewCombate

controller_jogador = ControllerJogador()
controller_npc = ControllerNpc()
controller_combate = ControllerCombate(ViewCombate(), controller_jogador, controller_npc)

controller_jogador.cadastrar_personagem("Jogador", CLASSE, 1)
controller_jogador.adicionar_poder_personagem("Jogador", PODER)
controller_jogador.cadastrar_personagem("Jogador2", CLASSE, 1)
controller_jogador.adicionar_poder_personagem("Jogador2", PODER)
controller_npc.cadastrar_personagem("Npc", CLASSE, 1)
controller_npc.adicionar_poder_personagem("Npc", PODER)


combate = Combate(1, controller_jogador.personagens, controller_npc.personagens)

controller_combate.cadastrar_combate(combate)

controller_combate.iniciar_combate(1)

