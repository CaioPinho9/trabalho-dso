from dao.dao import DAO
from exceptions import exceptions
from models.poder import Poder


class PoderDAO(DAO):

    def __init__(self):
        super().__init__('data/poderes.pkl')

    def add(self, poder: Poder, **kwargs):
        if not isinstance(poder, Poder):
            raise TypeError("poder deve ser um Poder")

        if not isinstance(poder.nome, str):
            raise TypeError("Key deve ser um string")

        try:
            self.get(poder.nome)
            raise exceptions.DuplicadoException(f"Poder com nome {poder.nome} já existe")
        except exceptions.NaoEncontradoException:
            pass

        super().add(poder.nome, poder)

    def update(self, poder: Poder, **kwargs):
        if not isinstance(poder, Poder):
            raise TypeError("poder deve ser um Poder")

        if not isinstance(poder.nome, str):
            raise TypeError("Key deve ser um string")

        super().update(poder.nome, poder)

    def get(self, key: str):
        if not isinstance(key, str):
            raise TypeError("Key deve ser um string")

        return super().get(key)

    def remove(self, key: str):
        """
        Deleta um poder por nome
        :param key: nome do poder deletado
        """
        if not isinstance(key, str):
            raise TypeError("Key deve ser um string")

        super().remove(key)
