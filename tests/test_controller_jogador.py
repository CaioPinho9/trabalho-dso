import pytest
from models.jogador import Jogador
from controllers.controller_jogador import ControllerJogador
from tests.default_models_to_test import CLASSE
from views.view_jogador import ViewJogador


def test_cadastrar_personagem():
    controller = ControllerJogador(ViewJogador())

    controller.cadastrar_personagem("Jogador1")

    assert len(controller.personagens) == 1
    assert isinstance(controller.personagens[0], Jogador)
    assert controller.personagens[0].nome == "Jogador1"
    assert controller.personagens[0].classe == CLASSE

def test_remover_personagem():
    controller = ControllerJogador(ViewJogador())
    classe = CLASSE
    controller.cadastrar_personagem("Jogador1")

    assert controller.remover_personagem("Jogador2") is False
    assert controller.remover_personagem("Jogador1") is True
    assert len(controller.personagens) == 0
