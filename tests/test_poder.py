import pytest
from models.poder import Poder


def test_criar_poder():
    poder = Poder('Fireball', 80, 120, 20, 1, True)
    assert poder.nome == 'Fireball'
    assert poder.acerto == 80
    assert poder.dano == 120
    assert poder.mana_gasta == 20
    assert poder.alvos == 1
    assert poder.ataque_cura


def test_criar_poder_invalido():
    with pytest.raises(TypeError):
        poder = Poder(1, 100, 0, 30, 3, True)
    with pytest.raises(TypeError):
        poder = Poder('Healing', "100", 0, 30, 3, True)
    with pytest.raises(TypeError):
        poder = Poder('Healing', 100, "0", 30, 3, True)
    with pytest.raises(TypeError):
        poder = Poder('Healing', 100, 0, "30", 3, True)
    with pytest.raises(TypeError):
        poder = Poder('Healing', 100, 0, 30, "3", True)
    with pytest.raises(TypeError):
        poder = Poder('Healing', 100, 0, 30, 3, 'false')
