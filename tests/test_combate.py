import pytest
from models.jogador import Jogador
from models.npc import Npc
from models.combate import Combate
from tests.default_models_to_test import CLASSE


def test_combate_init():
    # Testa se uma exceção é lançada quando o código não é um inteiro
    with pytest.raises(TypeError):
        Combate("codigo", [], [])

    # Testa se uma exceção é lançada quando jogadores não é uma lista
    with pytest.raises(TypeError):
        Combate(1, {}, [])

    # Testa se uma exceção é lançada quando npcs não é uma lista
    with pytest.raises(TypeError):
        Combate(1, [], {})

    # Testa se uma exceção é lançada quando jogadores não são do tipo Jogador
    with pytest.raises(TypeError):
        Combate(1, [1, 2, 3], [])

    # Testa se uma exceção é lançada quando npcs não são do tipo Npc
    with pytest.raises(TypeError):
        Combate(1, [], [1, 2, 3])

    # Testa se uma exceção é lançada quando não há jogadores
    with pytest.raises(ValueError):
        Combate(1, [], [Npc("Monstro", CLASSE)])

    # Testa se uma exceção é lançada quando não há npcs
    with pytest.raises(ValueError):
        Combate(1, [Jogador("Guerreiro", CLASSE)], [])


def test_combate_proximo_da_batalha():
    # Testa se uma exceção é lançada quando não há jogadores
    with pytest.raises(ValueError):
        combate = Combate(1, [], [Npc("Monstro", CLASSE)])

    # Testa se uma exceção é lançada quando não há npcs
    with pytest.raises(ValueError):
        combate = Combate(1, [Jogador("Guerreiro", CLASSE)], [])
    jogador = Jogador("Guerreiro", CLASSE)
    npc = Npc("Monstro", CLASSE)
    # Testa se o próximo da batalha é o personagem correto
    combate = Combate(1, [jogador], [npc])
    combate.ordem_de_batalha = [jogador, npc]
    assert combate.proximo_da_batalha().nome == "Guerreiro"
    assert combate.proximo_da_batalha().nome == "Monstro"
