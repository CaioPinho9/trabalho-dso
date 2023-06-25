from abc import abstractmethod

from dao.dao import DAO
from exceptions import exceptions
from models.personagem import Personagem


class PersonagemDAO(DAO):
    @abstractmethod
    def __init__(self, arquivo):
        super().__init__(arquivo)

    def add(self, personagem: Personagem, **kwargs):
        if not isinstance(personagem, Personagem):
            raise TypeError("personagem deve ser um Personagem")

        if not isinstance(personagem.nome, str):
            raise TypeError("Key deve ser uma string")

        try:
            self.get(personagem.nome)
            raise exceptions.DuplicadoException(f"Personagem com nome {personagem.nome} já existe")
        except exceptions.NaoEncontradoException:
            pass

        super().add(personagem.nome, personagem)

    def update(self, personagem: Personagem, **kwargs):
        if not isinstance(personagem, Personagem):
            raise TypeError("personagem deve ser um Personagem")

        if not isinstance(personagem.nome, str):
            raise TypeError("Key deve ser uma string")

        super().update(personagem.nome, personagem)

    def get(self, key: str):
        if not isinstance(key, str):
            raise TypeError("Key deve ser uma string")

        return super().get(key)

    def remove(self, key: str):
        """
        Deleta um personagem por nome
        :param key: nome do personagem deletado
        """
        if not isinstance(key, str):
            raise TypeError("Key deve ser uma string")

        super().remove(key)
