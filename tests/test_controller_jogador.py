import pytest
from models.classe import Classe
from models.jogador import Jogador
from models.poder import Poder
from models.item import Item
from controllers.controller_jogador import ControllerJogador


def test_cadastrar_personagem():
    controller = ControllerJogador()
    classe = Classe("Guerreiro")
    
    controller.cadastrar_personagem("Jogador1", classe, 1)

    assert len(controller.personagens) == 1
    assert isinstance(controller.personagens[0], Jogador)
    assert controller.personagens[0].nome == "Jogador1"
    assert controller.personagens[0].classe == classe
    assert controller.personagens[0].nivel == 1


def test_calcular_ataque():
    controller = ControllerJogador()
    poder = Poder("Fireball", 10)

    with pytest.raises(TypeError):
        controller.calcular_ataque("Poder")

    assert controller.calcular_ataque(poder) == 10


def test_calcular_buff():
    controller = ControllerJogador()
    item = Item("Item1", 5)

    with pytest.raises(TypeError):
        controller.calcular_buff("Item")

    assert controller.calcular_buff(item) == 5


def test_adicionar_item():
    controller = ControllerJogador()
    item = Item("Item1", 5)

    with pytest.raises(TypeError):
        controller.adicionar_item("Item")

    assert controller.adicionar_item(item) is False
    controller.remover_item(item)
    assert controller.adicionar_item(item) is True


def test_remover_item():
    controller = ControllerJogador()
    item = Item("Item1", 5)

    with pytest.raises(TypeError):
        controller.remover_item("Item")

    assert controller.remover_item(item) is False
    controller.adicionar_item(item)
    assert controller.remover_item(item) is True
    assert controller.get_item("Item1") is None


def test_remover_personagem():
    controller = ControllerJogador()
    classe = Classe("Guerreiro")
    controller.cadastrar_personagem("Jogador1", classe, 1)

    assert controller.remover_personagem("Jogador2") is False
    assert controller.remover_personagem("Jogador1") is True
    assert len(controller.personagens) == 0
