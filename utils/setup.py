from controllers.controller_classe import ControllerClasse
from controllers.controller_combate import ControllerCombate
from controllers.controller_jogador import ControllerJogador
from controllers.controller_npc import ControllerNpc
from controllers.controller_poder import ControllerPoder

CLASSES = [
    {
        "nome": "Mago Estudante",
        "vida": 10,
        "velocidade": 2,
        "defesa": 12,
        "mana": 30,
        "nivel": 1,
        "tipo": "Mago"
    },
    {
        "nome": "Guerreiro Novato",
        "vida": 30,
        "velocidade": -2,
        "defesa": 16,
        "mana": 10,
        "nivel": 1,
        "tipo": "Guerreiro"
    },
    {
        "nome": "Ladino Aprendiz",
        "vida": 15,
        "velocidade": 5,
        "defesa": 15,
        "mana": 15,
        "nivel": 1,
        "tipo": "Ladino"
    },
    {
        "nome": "Mago",
        "vida": 20,
        "velocidade": 2,
        "defesa": 12,
        "mana": 40,
        "nivel": 2,
        "tipo": "Mago"
    },
    {
        "nome": "Guerreiro",
        "vida": 40,
        "velocidade": -2,
        "defesa": 17,
        "mana": 12,
        "nivel": 2,
        "tipo": "Guerreiro"
    },
    {
        "nome": "Ladino",
        "vida": 30,
        "velocidade": 5,
        "defesa": 15,
        "mana": 20,
        "nivel": 2,
        "tipo": "Ladino"
    },
    {
        "nome": "Arquimago",
        "vida": 30,
        "velocidade": 2,
        "defesa": 13,
        "mana": 50,
        "nivel": 3,
        "tipo": "Mago"
    },
    {
        "nome": "Guerreiro Mestre",
        "vida": 50,
        "velocidade": -2,
        "defesa": 19,
        "mana": 15,
        "nivel": 3,
        "tipo": "Guerreiro"
    },
    {
        "nome": "Ladino Chefe",
        "vida": 40,
        "velocidade": 8,
        "defesa": 16,
        "mana": 25,
        "nivel": 3,
        "tipo": "Ladino"
    },
    {
        "nome": "Minion",
        "vida": 10,
        "velocidade": 5,
        "defesa": 10,
        "mana": 5,
        "nivel": 0,
        "tipo": None
    },
    {
        "nome": "Boss",
        "vida": 120,
        "velocidade": -4,
        "defesa": 14,
        "mana": 30,
        "nivel": 5,
        "tipo": None
    }
]

PODERES = [
    {
        "nome": "Soco",
        "acerto": 0,
        "dano": 1,
        "mana_gasta": 0,
        "alvos": 1,
        "ataque": True,
        "nivel": 0
    },
    # Curas, gasto de mana médio,
    {
        "nome": "Cura Inferior",
        "acerto": 10,
        "dano": 10,
        "mana_gasta": 5,
        "alvos": 1,
        "ataque": False,
        "nivel": 1
    },
    {
        "nome": "Cura Regular",
        "acerto": 10,
        "dano": 15,
        "mana_gasta": 7,
        "alvos": 1,
        "ataque": False,
        "nivel": 2
    },
    {
        "nome": "Cura Superior",
        "acerto": 10,
        "dano": 20,
        "mana_gasta": 8,
        "alvos": 1,
        "ataque": False,
        "nivel": 3
    },
    # Sem gasto de mana, porem dano medio e acerto medio
    {
        "nome": "Espada de Bronze",
        "acerto": 7,
        "dano": 8,
        "mana_gasta": 0,
        "alvos": 1,
        "ataque": True,
        "nivel": 1
    },
    {
        "nome": "Espada de Aço",
        "acerto": 8,
        "dano": 10,
        "mana_gasta": 0,
        "alvos": 1,
        "ataque": True,
        "nivel": 2
    },
    {
        "nome": "Espada de Adamantio",
        "acerto": 9,
        "dano": 12,
        "mana_gasta": 0,
        "alvos": 1,
        "ataque": True,
        "nivel": 3
    },
    # Sem gasto de mana, porem dano baixo e acerto alto
    {
        "nome": "Adaga de Bronze",
        "acerto": 9,
        "dano": 4,
        "mana_gasta": 0,
        "alvos": 1,
        "ataque": True,
        "nivel": 1
    },
    {
        "nome": "Adaga de Aço",
        "acerto": 11,
        "dano": 6,
        "mana_gasta": 0,
        "alvos": 1,
        "ataque": True,
        "nivel": 2
    },
    {
        "nome": "Adaga de Adamantio",
        "acerto": 13,
        "dano": 8,
        "mana_gasta": 0,
        "alvos": 1,
        "ataque": True,
        "nivel": 3
    },
    # Ataques em área, gasto de mana medio/alto, porem dano alto e acerto alto
    {
        "nome": "Ataque Giratório",
        "acerto": 5,
        "dano": 5,
        "mana_gasta": 3,
        "alvos": 2,
        "ataque": True,
        "nivel": 1
    },
    {
        "nome": "Golpe Poderoso",
        "acerto": 4,
        "dano": 20,
        "mana_gasta": 4,
        "alvos": 1,
        "ataque": True,
        "nivel": 1
    },
    {
        "nome": "Raio de Fogo",
        "acerto": 5,
        "dano": 6,
        "mana_gasta": 4,
        "alvos": 3,
        "ataque": True,
        "nivel": 1
    },
    {
        "nome": "Bola de Fogo",
        "acerto": 7,
        "dano": 10,
        "mana_gasta": 10,
        "alvos": 3,
        "ataque": True,
        "nivel": 2
    },
    {
        "nome": "Golpe Esmagador",
        "acerto": 3,
        "dano": 20,
        "mana_gasta": 10,
        "alvos": 2,
        "ataque": True,
        "nivel": 3
    },
    {
        "nome": "Lançamento de Pedras",
        "acerto": 6,
        "dano": 10,
        "mana_gasta": 15,
        "alvos": 2,
        "ataque": True,
        "nivel": 4
    }
]

NPCS = [
    {
        "nome": "Hobgoblin",
        "classe": "Guerreiro Novato",
        "poderes": [
            "Espada de Aço",
            "Ataque Giratório",
            "Golpe Poderoso"
        ]
    },
    {
        "nome": "Kobold",
        "classe": "Ladino Aprendiz",
        "poderes": [
            "Adaga de Aço"
        ]
    },
    {
        "nome": "Rei Gnomo",
        "classe": "Boss",
        "poderes": [
            "Golpe Esmagador",
            "Lançamento de Pedras",
            "Espada de Adamantio"
        ]
    }
]
for i in range(1, 8):
    NPCS.append(
        {
            "nome": f"Gnomo{i}",
            "classe": "Minion",
            "poderes": [
                "Adaga de Aço",
                "Ataque Giratório"
            ]
        }
    )

JOGADORES = [
    {
        "nome": "Jorge",
        "classe": "Mago Estudante",
        "poderes": [
            "Raio de Fogo",
            "Adaga de Bronze",
            "Cura Inferior"
        ]
    },
    {
        "nome": "João",
        "classe": "Guerreiro Novato",
        "poderes": [
            "Ataque Giratório",
            "Espada de Bronze",
            "Golpe Poderoso"
        ]
    },
    {
        "nome": "Jaime",
        "classe": "Ladino Aprendiz",
        "poderes": [
            "Ataque Giratório",
            "Adaga de Bronze",
            "Raio de Fogo"
        ]
    }
]

COMBATES = [
    {
        "npcs": ["Kobold", "Hobgoblin"]
    },
    {
        "npcs": ["Gnomo1", "Gnomo2", "Gnomo3", "Gnomo4", "Gnomo5", "Gnomo6", "Gnomo7"]
    },
    {
        "npcs": ["Rei Gnomo", "Gnomo1", "Gnomo2", "Gnomo3"]
    },
]


def setup(controller_classe: ControllerClasse, controller_poder: ControllerPoder, controller_npc: ControllerNpc,
          controller_jogador: ControllerJogador, controller_combate: ControllerCombate):
    # Gerar classes
    controller_classe.remover_all()
    for classe in CLASSES:
        controller_classe.cadastrar(
            nome=classe["nome"],
            vida=classe["vida"],
            velocidade=classe["velocidade"],
            defesa=classe["defesa"],
            mana=classe["mana"],
            nivel=classe["nivel"],
            tipo=classe["tipo"]
        )

    # Gerar poderes
    controller_poder.remover_all()
    for poder in PODERES:
        controller_poder.cadastrar(
            nome=poder["nome"],
            acerto=poder["acerto"],
            dano=poder["dano"],
            mana_gasta=poder["mana_gasta"],
            alvos=poder["alvos"],
            ataque=poder["ataque"],
            nivel=poder["nivel"]
        )

    # Gerar jogadores
    controller_jogador.remover_all()
    for jogador in JOGADORES:
        controller_jogador.cadastrar(
            nome=jogador["nome"],
            classe=controller_classe.get(jogador["classe"]),
            poderes=[controller_poder.get(nome) for nome in jogador["poderes"]]
        )

    # Gerar npcs
    controller_npc.remover_all()
    for npc in NPCS:
        controller_npc.cadastrar(
            nome=npc["nome"],
            classe=controller_classe.get(npc["classe"]),
            poderes=[controller_poder.get(nome_poder) for nome_poder in npc["poderes"]]
        )

    # Gerar combates
    controller_combate.remover_all()
    for combate in COMBATES:
        controller_combate.cadastrar(
            npcs=[controller_npc.get(npc_nome) for npc_nome in combate["npcs"]],
        )
