import pytest
from models.classe import Classe
from models.poder import Poder
from models.personagem import Personagem


def test_personagem_init():
    # Test initialization with valid arguments
    nome = "Teste"
    classe = Classe("classe", 10, 10, 10, 10)
    nivel = 1
    personagem = Personagem(nome, classe)
    assert personagem.nome == nome
    assert personagem.classe == classe

    # Test initialization with invalid arguments
    with pytest.raises(TypeError):
        Personagem(123, classe)
    with pytest.raises(TypeError):
        Personagem(nome, "invalid_class")
    with pytest.raises(TypeError):
        Personagem(nome, classe)

def test_personagem_adicionar_poder():
    # Test adding a valid power
    nome = "Teste"
    classe = Classe("classe", 10, 10, 10, 10)
    nivel = 1
    personagem = Personagem(nome, classe)
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
    personagem = Personagem(nome, classe)
    poder = Poder("Ataque", 1, 1, 1, 1, True)
    personagem.adicionar_poder(poder)
    personagem.remover_poder("Ataque")
    assert len(personagem.poderes) == 0

    # Test removing a non-existing power
    personagem.adicionar_poder(poder)
    assert not personagem.remover_poder("invalid_power")
    assert len(personagem.poderes) == 1

