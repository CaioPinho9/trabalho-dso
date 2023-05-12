from models.classe import Classe
from models.jogador import Jogador
from models.npc import Npc
from models.poder import Poder

CLASSE = Classe("Classe", 20, 5, 5, 10)

PODER = Poder('Firebolt', 3, 12, 3, 1, True)

JOGADOR = Jogador("Jogador", CLASSE, 1)

NPC = Npc("NPC", CLASSE, 1)

