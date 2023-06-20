from dao.dao import DAO
from exceptions import exceptions
from models.combate import Combate


class CombateDAO(DAO):
    def __init__(self):
        super().__init__('data/combates.pkl')

    def add(self, combate: Combate, **kwargs):
        if not isinstance(combate, Combate):
            raise TypeError("combate deve ser um Combate")

        if not isinstance(combate.codigo, int):
            raise TypeError("Key deve ser uma integer")

        try:
            self.get(combate.codigo)
            raise exceptions.DuplicadoException(f"Combate com codigo {combate.codigo} já existe")
        except exceptions.NaoEncontradoException:
            pass

        super().add(combate.codigo, combate)

    def update(self, combate: Combate, **kwargs):
        if not isinstance(combate, Combate):
            raise TypeError("combate deve ser um Combate")

        if not isinstance(combate.codigo, int):
            raise TypeError("Key deve ser uma integer")

        super().update(combate.codigo, combate)

    def get(self, key: int):
        if not isinstance(key, int):
            raise TypeError("Key deve ser uma integer")

        return super().get(key)

    def remove(self, key: int):
        """
        Deleta um combate por codigo
        :param key: codigo do combate deletado
        """
        if not isinstance(key, int):
            raise TypeError("Key deve ser uma integer")

        super().remove(key)
