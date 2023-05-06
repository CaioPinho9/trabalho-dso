from exceptions.exceptions import DuplicadoException, NaoEncontradoException
from models.classe import Classe


class ControllerClasse:
    def __init__(self):
        self.__classe = []

    def cadastrar_classe(self, classe):
        """
        Cadastra uma nova classe na lista de classes.

        Parâmetros:
        classe (Classe): objeto Classe a ser cadastrado.

        Lança:
        TypeError: caso o objeto passado não seja uma instância válida de Classe.
        DuplicadoException: caso já exista uma Classe com o mesmo nome na lista de classes.

        Retorno:
        True.
        """
        if not isinstance(classe, Classe):
            raise TypeError("Não é uma classe")

        if self.get_classe(classe.nome):
            raise DuplicadoException('Não foi possivel criar a classe pois ja existe uma com o mesmo nome')

        self.__classe.append(classe)

        return True

    def remover_classe(self, nome):
        """
        Remove uma classe da lista de classes.

        Parâmetros:
        nome (str): nome da classe a ser removido.

        Lança:
        NaoEncontradoException: caso não exista uma Classe com o nome passado na lista de classes.

        Retorno:
        True.
        """
        classe = self.get_classe(nome)
        if not classe:
            raise NaoEncontradoException("A classe não foi encontrada")

        self.__classe.remove(classe)

        return True

    def get_classe(self, nome):
        """
        Obtém uma classe da lista de classes.

        Parâmetros:
        nome (str): nome da Classe a ser encontrado.

        Retorno:
        Classe: objeto Classe com o mesmo nome, caso encontrado; ou None, caso não encontrado.
        """
        for classe in self.__classe:
            if classe.nome == nome:
                return classe
        return None
