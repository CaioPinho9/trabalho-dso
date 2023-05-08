from controllers.controller_jogador import ControllerJogador
from controllers.controller_npc import ControllerNpc
from models.classe import Classe
from models.jogador import Jogador
from models.npc import Npc
from models.poder import Poder


def test_cadastrar_jogador():
    controller = ControllerJogador()
    classe = Classe("classe", 10, 10, 10, 10)
    controller.cadastrar_personagem("Gandalf", classe, 10)
    assert len(controller.personagens) == 1


def test_remover_jogador():
    controller = ControllerJogador()
    classe = Classe("classe", 10, 10, 10, 10)
    controller.cadastrar_personagem("Gandalf", classe, 10)
    controller.remover_personagem("Gandalf")
    assert len(controller.personagens) == 0


def test_adicionar_poder_jogador():
    controller = ControllerJogador()
    poder = Poder('Fireball', 80, 120, 20, 1, True)
    classe = Classe("classe", 10, 10, 10, 10)
    controller.cadastrar_personagem("Gandalf", classe, 10)
    controller.adicionar_poder_personagem("Gandalf", poder)
    personagem = controller.get_personagem("Gandalf")
    assert len(personagem.poderes) == 1


def test_remover_poder_jogador():
    controller = ControllerJogador()
    poder = Poder('Fireball', 80, 120, 20, 1, True)
    classe = Classe("classe", 10, 10, 10, 10)
    controller.cadastrar_personagem("Gandalf", classe, 10)
    controller.adicionar_poder_personagem("Gandalf", poder)
    controller.remover_poder_personagem("Gandalf", "Fireball")
    personagem = controller.get_personagem("Gandalf")
    assert len(personagem.poderes) == 0


def test_get_jogador():
    controller = ControllerJogador()
    classe = Classe("classe", 10, 10, 10, 10)
    controller.cadastrar_personagem("Gandalf", classe, 10)
    personagem = controller.get_personagem("Gandalf")
    assert isinstance(personagem, Jogador)
    assert personagem.nome == "Gandalf"
    assert personagem.classe == classe
    assert personagem.nivel == 10


def test_calcular_poder_jogador():
    controller = ControllerJogador()
    poder = Poder('Fireball', 80, 120, 20, 1, True)
    dano, resultado_acerto = controller.calcular_poder(poder)
    assert isinstance(dano, int)
    assert isinstance(resultado_acerto, int)


def test_cadastrar_npc():
    controller = ControllerNpc()
    classe = Classe("classe", 10, 10, 10, 10)
    controller.cadastrar_personagem("Gandalf", classe, 10)
    assert len(controller.personagens) == 1


def test_remover_npc():
    controller = ControllerNpc()
    classe = Classe("classe", 10, 10, 10, 10)
    controller.cadastrar_personagem("Gandalf", classe, 10)
    controller.remover_personagem("Gandalf")
    assert len(controller.personagens) == 0


def test_adicionar_poder_npc():
    controller = ControllerNpc()
    poder = Poder('Fireball', 80, 120, 20, 1, True)
    classe = Classe("classe", 10, 10, 10, 10)
    controller.cadastrar_personagem("Gandalf", classe, 10)
    controller.adicionar_poder_personagem("Gandalf", poder)
    personagem = controller.get_personagem("Gandalf")
    assert len(personagem.poderes) == 1


def test_remover_poder_npc():
    controller = ControllerNpc()
    poder = Poder('Fireball', 80, 120, 20, 1, True)
    classe = Classe("classe", 10, 10, 10, 10)
    controller.cadastrar_personagem("Gandalf", classe, 10)
    controller.adicionar_poder_personagem("Gandalf", poder)
    controller.remover_poder_personagem("Gandalf", "Fireball")
    personagem = controller.get_personagem("Gandalf")
    assert len(personagem.poderes) == 0


def test_get_npc():
    controller = ControllerNpc()
    classe = Classe("classe", 10, 10, 10, 10)
    controller.cadastrar_personagem("Gandalf", classe, 10)
    personagem = controller.get_personagem("Gandalf")
    assert isinstance(personagem, Npc)
    assert personagem.nome == "Gandalf"
    assert personagem.classe == classe
    assert personagem.nivel == 10


def test_calcular_poder_npc():
    controller = ControllerNpc()
    poder = Poder('Fireball', 80, 120, 20, 1, True)
    dano, resultado_acerto = controller.calcular_poder(poder)
    assert isinstance(dano, int)
    assert isinstance(resultado_acerto, int)
