import pytest
from models.jogador import Jogador
from tests.default_models_to_test import CLASSE


def test_jogador_init():
    jogador = Jogador("John", CLASSE)

    assert jogador.nome == "John"
    assert jogador.classe == CLASSE
    assert jogador.dano_recebido == 0


def test_jogador_init_invalid_types():
    with pytest.raises(TypeError):
        Jogador(123, CLASSE)
    with pytest.raises(TypeError):
        Jogador("John", "Guerreiro")


def test_jogador_dano_causado():
    jogador = Jogador("John", CLASSE)
    jogador.dano_causado = 50

    assert jogador.dano_causado == 50


def test_jogador_dano_causado_invalid_type():
    jogador = Jogador("John", CLASSE)

    with pytest.raises(TypeError):
        jogador.dano_causado = "cinquenta"


def test_jogador_dano_recebido():
    jogador = Jogador("John", CLASSE)
    jogador.dano_recebido = 30

    assert jogador.dano_recebido == 30


def test_jogador_dano_recebido_invalid_type():
    jogador = Jogador("John", CLASSE)

    with pytest.raises(TypeError):
        jogador.dano_recebido = "trinta"


def test_jogador_properties_readonly():
    jogador = Jogador("John", CLASSE)

    with pytest.raises(AttributeError):
        jogador.nome = "Jane"
    with pytest.raises(AttributeError):
        jogador.classe = CLASSE


def test_jogador_properties_setter_for_private_attributes():
    jogador = Jogador("John", CLASSE)

    with pytest.raises(AttributeError):
        jogador.__dano_causado = 50
    with pytest.raises(AttributeError):
        jogador.__dano_recebido = 30
