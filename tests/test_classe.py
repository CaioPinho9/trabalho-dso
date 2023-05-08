import pytest
from models.classe import Classe


def test_classe_init():
    # Test initialization with valid arguments
    nome = "Guerreiro"
    vida = 100
    velocidade = 10
    defesa = 50
    mana = 0
    classe = Classe(nome, vida, velocidade, defesa, mana)
    assert classe.nome == nome
    assert classe.vida == vida
    assert classe.velocidade == velocidade
    assert classe.defesa == defesa
    assert classe.mana == mana

    # Test initialization with invalid arguments
    with pytest.raises(TypeError):
        Classe(123, vida, velocidade, defesa, mana)
    with pytest.raises(TypeError):
        Classe(nome, "invalid_vida", velocidade, defesa, mana)
    with pytest.raises(TypeError):
        Classe(nome, vida, "invalid_velocidade", defesa, mana)
    with pytest.raises(TypeError):
        Classe(nome, vida, velocidade, "invalid_defesa", mana)
    with pytest.raises(TypeError):
        Classe(nome, vida, velocidade, defesa, "invalid_mana")
