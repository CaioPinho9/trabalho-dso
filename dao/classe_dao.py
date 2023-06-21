from dao.dao import DAO
from exceptions import exceptions
from models.classe import Classe


class ClasseDAO(DAO):

    def __init__(self):
        super().__init__('data/classes.pkl')

    def add(self, classe: Classe, **kwargs):
        if not isinstance(classe, Classe):
            raise TypeError("classe deve ser uma Classe")

        if not isinstance(classe.nome, str):
            raise TypeError("Key deve ser uma string")

        try:
            self.get(classe.nome)
            raise exceptions.DuplicadoException(f"Classe com nome {classe.nome} já existe")
        except exceptions.NaoEncontradoException:
            pass

        super().add(classe.nome, classe)

    def update(self, classe: Classe, **kwargs):
        if not isinstance(classe, Classe):
            raise TypeError("classe deve ser uma Classe")

        if not isinstance(classe.nome, str):
            raise TypeError("Key deve ser uma string")

        super().update(classe.nome, classe)

    def get(self, key: str):
        if not isinstance(key, str):
            raise TypeError("Key deve ser uma string")

        return super().get(key)

    def remove(self, key: str):
        """
        Deleta uma classe por nome
        :param key: nome da classe deletado
        """
        if not isinstance(key, str):
            raise TypeError("Key deve ser uma string")

        super().remove(key)
