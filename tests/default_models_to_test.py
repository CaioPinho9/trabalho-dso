from models.classe import Classe
from models.jogador import Jogador
from models.npc import Npc
from models.poder import Poder

CLASSE = Classe("Classe", 10, 5, 5, 5)

PODER = Poder('Poder', 3, 12, 3, 1, True)

JOGADOR = Jogador("Jogador", CLASSE, 1)

NPC = Npc("NPC", CLASSE, 1)

