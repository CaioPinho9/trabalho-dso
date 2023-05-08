import pytest
from models.classe import Classe
from models.poder import Poder
from models.personagem import Personagem


def test_personagem_init():
    # Test initialization with valid arguments
    nome = "Teste"
    classe = Classe("classe", 10, 10, 10, 10)
    nivel = 1
    personagem = Personagem(nome, classe, nivel)
    assert personagem.nome == nome
    assert personagem.classe == classe
    assert personagem.nivel == nivel

    # Test initialization with invalid arguments
    with pytest.raises(TypeError):
        Personagem(123, classe, nivel)
    with pytest.raises(TypeError):
        Personagem(nome, "invalid_class", nivel)
    with pytest.raises(TypeError):
        Personagem(nome, classe, "invalid_level")


def test_personagem_aumentar_nivel():
    # Test increasing level
    nome = "Teste"
    classe = Classe("classe", 10, 10, 10, 10)
    nivel = 1
    personagem = Personagem(nome, classe, nivel)
    personagem.aumentar_nivel()
    assert personagem.nivel == 2


def test_personagem_adicionar_poder():
    # Test adding a valid power
    nome = "Teste"
    classe = Classe("classe", 10, 10, 10, 10)
    nivel = 1
    personagem = Personagem(nome, classe, nivel)
    poder = Poder("Ataque", 1, 1, 1, 1, True)
    personagem.adicionar_poder(poder)
    assert len(personagem.poderes) == 1
    assert personagem.poderes[0] == poder

    # Test adding an invalid power
    with pytest.raises(TypeError):
        personagem.adicionar_poder("invalid_power")


def test_personagem_remover_poder():
    # Test removing an existing power
    nome = "Teste"
    classe = Classe("classe", 10, 10, 10, 10)
    nivel = 1
    personagem = Personagem(nome, classe, nivel)
    poder = Poder("Ataque", 1, 1, 1, 1, True)
    personagem.adicionar_poder(poder)
    personagem.remover_poder("Ataque")
    assert len(personagem.poderes) == 0

    # Test removing a non-existing power
    personagem.adicionar_poder(poder)
    assert not personagem.remover_poder("invalid_power")
    assert len(personagem.poderes) == 1

