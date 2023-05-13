from exceptions.exceptions import DuplicadoException, NaoEncontradoException
from models.classe import Classe


class ControllerClasse:
    def __init__(self):
        self.__classes = []

    def cadastrar_classe(self, nome: str, vida: int, velocidade: int, defesa: int, mana: int):
        classe = Classe(nome, vida, velocidade, defesa, mana)

        if self.get_classe(classe.nome):
            raise DuplicadoException('Não foi possivel criar a classe pois ja existe uma com o mesmo nome')

        self.__classes.append(classe)

        return True

    @property
    def classes(self):
        return self.__classes

    def remover_classe(self, nome: str):
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

        self.__classes.remove(classe)

        return True

    def get_classe(self, nome: str):
        """
        Obtém uma classe da lista de classes.

        Parâmetros:
        nome (str): nome da Classe a ser encontrado.

        Retorno:
        Classe: objeto Classe com o mesmo nome, caso encontrado; ou None, caso não encontrado.
        """
        if not isinstance(nome, str):
            raise TypeError("nome deve ser uma string")

        for classe in self.__classes:
            if classe.nome == nome:
                return classe
        return None

    def get_classe_por_index(self, index: int):
        """
        Obtém uma classe da lista de classes.

        Parâmetros:
        index (int): nome da Classe a ser encontrado.

        Retorno:
        Classe: objeto Classe com o mesmo nome, caso encontrado; ou None, caso não encontrado.
        """
        if not isinstance(index, int):
            raise TypeError("index deve ser uma string")

        try:
            classe = self.__classes[index]
            return classe
        except Exception:
            return None

    def classe_estatisticas(self):
        estatisticas = [classe.nome + "["+str(index)+"]: \nVida: " + str(classe.vida) +
                        "\nDefesa: " + str(classe.defesa) +
                        "\nMana: " + str(classe.mana) +
                        "\nVelocidade: " + str(classe.velocidade)
                        for index, classe in enumerate(self.__classes)]
        return "\n-------------------\n".join(estatisticas)
