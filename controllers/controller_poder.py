from exceptions.exceptions import DuplicadoException, NaoEncontradoException
from models.poder import Poder


class ControllerPoder:
    def __init__(self):
        self.__poderes = []

    def cadastrar_poder(self, poder: Poder):
        """
        Cadastra um novo objeto Poder na lista de poderes.

        Parâmetros:
        poder (Poder): objeto Poder a ser cadastrado.

        Lança:
        TypeError: caso o objeto passado não seja uma instância válida de Poder.
        DuplicadoException: caso já exista um objeto Poder com o mesmo nome na lista de poderes.

        Retorno:
        True.
        """
        if not isinstance(poder, Poder):
            raise TypeError("Não é um poder")

        if self.get_poder(poder.nome):
            raise DuplicadoException('Não foi possivel criar o poder pois ja existe um com o mesmo nome')

        self.__poderes.append(poder)

        return True

    def remover_poder(self, nome: str):
        """
        Remove um objeto Poder da lista de poderes.

        Parâmetros:
        nome (str): nome do objeto Poder a ser removido.

        Lança:
        NaoEncontradoException: caso não exista um objeto Poder com o nome passado na lista de poderes.

        Retorno:
        True.
        """
        poder = self.get_poder(nome)
        if not poder:
            raise NaoEncontradoException("O poder não foi encontrado.")

        self.__poderes.remove(poder)

        return True

    def get_poder(self, nome: str):
        """
        Obtém um objeto Poder da lista de poderes.

        Parâmetros:
        nome (str): nome do objeto Poder a ser encontrado.

        Retorno:
        Poder: objeto Poder com o mesmo nome, caso encontrado; ou None, caso não encontrado.
        """
        for poder in self.__poderes:
            if poder.nome == nome:
                return poder
        return None
