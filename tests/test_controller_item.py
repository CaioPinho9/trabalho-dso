import pytest
from models.item import Item
from exceptions.exceptions import DuplicadoException
from controllers.controller_item import ControllerItem


def test_criar_item():
    controller = ControllerItem()
    item = Item("item1")

    assert controller.criar_item(item) is True
    assert controller.get_item("item1") == item

    with pytest.raises(TypeError):
        controller.criar_item("item2")

    with pytest.raises(DuplicadoException):
        controller.criar_item(item)


def test_remover_item():
    controller = ControllerItem()
    item1 = Item("item1")
    item2 = Item("item2")

    controller.criar_item(item1)
    controller.criar_item(item2)

    with pytest.raises(TypeError):
        controller.remover_item("item1")

    assert controller.remover_item(Item("item3")) is False
    assert controller.remover_item(item1) is True
    assert controller.get_item("item1") is None


def test_get_item():
    controller = ControllerItem()
    item1 = Item("item1")
    item2 = Item("item2")

    controller.criar_item(item1)
    controller.criar_item(item2)

    assert controller.get_item("item1") == item1
    assert controller.get_item("item2") == item2
    assert controller.get_item("item3") is None
