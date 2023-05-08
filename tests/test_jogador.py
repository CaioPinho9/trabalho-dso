import pytest
from models.personagem import Personagem
from models.item import Item
from models.classe import Classe
from models.jogador import Jogador

def test_jogador_init():
    classe = Classe("Guerreiro")
    jogador = Jogador("John", classe, 1)

    assert jogador.nome == "John"
    assert jogador.classe == classe
    assert jogador.nivel == 1
    assert jogador.dano_causado == 0
    assert jogador.dano_recebido == 0
    assert jogador.itens == []

def test_jogador_init_invalid_types():
    with pytest.raises(TypeError):
        Jogador(123, Classe("Guerreiro"), 1)
    with pytest.raises(TypeError):
        Jogador("John", "Guerreiro", 1)
    with pytest.raises(TypeError):
        Jogador("John", Classe("Guerreiro"), "um")

def test_jogador_dano_causado():
    classe = Classe("Guerreiro")
    jogador = Jogador("John", classe, 1)
    jogador.dano_causado = 50

    assert jogador.dano_causado == 50

def test_jogador_dano_causado_invalid_type():
    classe = Classe("Guerreiro")
    jogador = Jogador("John", classe, 1)

    with pytest.raises(TypeError):
        jogador.dano_causado = "cinquenta"

def test_jogador_dano_recebido():
    classe = Classe("Guerreiro")
    jogador = Jogador("John", classe, 1)
    jogador.dano_recebido = 30

    assert jogador.dano_recebido == 30

def test_jogador_dano_recebido_invalid_type():
    classe = Classe("Guerreiro")
    jogador = Jogador("John", classe, 1)

    with pytest.raises(TypeError):
        jogador.dano_recebido = "trinta"

def test_jogador_adicionar_item():
    classe = Classe("Guerreiro")
    jogador = Jogador("John", classe, 1)
    item = Item("Espada", "Arma")

    jogador.adicionar_item(item)

    assert item in jogador.itens

def test_jogador_adicionar_item_invalid_type():
    classe = Classe("Guerreiro")
    jogador = Jogador("John", classe, 1)

    with pytest.raises(TypeError):
        jogador.adicionar_item("Espada")

def test_jogador_remover_item():
    classe = Classe("Guerreiro")
    jogador = Jogador("John", classe, 1)
    item = Item("Espada", "Arma")
    jogador.adicionar_item(item)

    jogador.remover_item(item)

    assert item not in jogador.itens

def test_jogador_adicionar_multiple_items():
    classe = Classe("Guerreiro")
    jogador = Jogador("John", classe, 1)
    item1 = Item("Espada", "Arma")
    item2 = Item("Escudo", "Defesa")

    jogador.adicionar_item(item1)
    jogador.adicionar_item(item2)

    assert item1 in jogador.itens
    assert item2 in jogador.itens
    assert len(jogador.itens) == 2

def test_jogador_remover_nonexistent_item():
    classe = Classe("Guerreiro")
    jogador = Jogador("John", classe, 1)
    item1 = Item("Espada", "Arma")
    item2 = Item("Escudo", "Defesa")

    jogador.adicionar_item(item1)

    with pytest.raises(ValueError):
        jogador.remover_item(item2)

def test_jogador_properties_readonly():
    classe = Classe("Guerreiro")
    jogador = Jogador("John", classe, 1)

    with pytest.raises(AttributeError):
        jogador.nome = "Jane"
    with pytest.raises(AttributeError):
        jogador.classe = Classe("Mago")
    with pytest.raises(AttributeError):
        jogador.nivel = 2
    with pytest.raises(AttributeError):
        jogador.itens = []

def test_jogador_properties_setter_for_private_attributes():
    classe = Classe("Guerreiro")
    jogador = Jogador("John", classe, 1)

    with pytest.raises(AttributeError):
        jogador.__dano_causado = 50
    with pytest.raises(AttributeError):
        jogador.__dano_recebido = 30
    with pytest.raises(AttributeError):
        jogador.__itens = []
