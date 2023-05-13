import pytest
from unittest.mock import MagicMock

from controllers.controller_combate import ControllerCombate
from exceptions.exceptions import NaoEncontradoException
from models.jogador import Jogador
from models.npc import Npc
from tests.default_models_to_test import CLASSE


class TestControllerCombate:
    @pytest.fixture
    def controller_combate(self):
        view_combate_mock = MagicMock()
        view_erro_mock = MagicMock()
        controller_jogador_mock = MagicMock()
        controller_npc_mock = MagicMock()
        controller_poder_mock = MagicMock()
        return ControllerCombate(view_combate_mock, view_erro_mock, controller_jogador_mock,
                                 controller_npc_mock, controller_poder_mock)

    @pytest.fixture
    def jogadores(self):
        jogador1 = Jogador("Jogador 1", CLASSE)
        jogador2 = Jogador("Jogador 2", CLASSE)
        jogador3 = Jogador("Jogador 3", CLASSE)
        return [jogador1, jogador2, jogador3]

    @pytest.fixture
    def npcs(self):
        npc1 = Npc("NPC 1", CLASSE)
        npc2 = Npc("NPC 2", CLASSE)
        npc3 = Npc("NPC 3", CLASSE)
        return [npc1, npc2, npc3]

    def test_cadastrar_combate(self, controller_combate, jogadores, npcs):
        controller_combate.cadastrar_combate(jogadores, npcs)
        assert len(controller_combate._ControllerCombate__combates) == 1

    def test_get_combate(self, controller_combate, jogadores, npcs):
        controller_combate.cadastrar_combate(jogadores, npcs)
        combate = controller_combate.get_combate(0)
        assert combate.jogadores == jogadores
        assert combate.npcs == npcs

    def test_get_combate_invalido(self, controller_combate):
        with pytest.raises(TypeError):
            controller_combate.get_combate("abc")

    def test_iniciar_combate(self, controller_combate, jogadores, npcs):
        controller_combate.cadastrar_combate(jogadores, npcs)
        controller_combate.iniciar_combate(0)
        assert controller_combate._ControllerCombate__combate_atual is not None

    def test_iniciar_combate_nao_encontrado(self, controller_combate):
        with pytest.raises(NaoEncontradoException):
            controller_combate.iniciar_combate(0)