from exceptions.exceptions import DuplicadoException, NaoEncontradoException
from models.classe import Classe


class ControllerClasse:
    def __init__(self):
        self.__classes = []

    def cadastrar_classe(self, nome: str, vida: int, velocidade: int, defesa: int, mana: int, nivel: int,
                         tipo: str = None):
        classe = Classe(nome, vida, velocidade, defesa, mana, nivel, tipo)

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
        :param nome: nome da classe a ser removido.
        :raise NaoEncontradoException: caso não exista uma Classe com o nome passado na lista de classes.
        :return: True
        """
        classe = self.get_classe(nome)
        if not classe:
            raise NaoEncontradoException("A classe não foi encontrada")

        self.__classes.remove(classe)

        return True

    def get_classe(self, nome: str):
        """
        Obtém uma classe da lista de classes.
        :param nome: nome da Classe a ser encontrado.
        :return: objeto Classe com o mesmo nome, caso encontrado; ou None, caso não encontrado.
        """
        if not isinstance(nome, str):
            raise TypeError("nome deve ser uma string")

        for classe in self.__classes:
            if classe.nome == nome:
                return classe
        return None

    def get_classes_por_nivel(self, nivel):
        """
        Retorna uma lista com as classes de certo nivel
        :param nivel: numero que determina a força de um classe
        :return: lista de classes do nivel pedido
        """
        if not isinstance(nivel, int):
            raise TypeError("nivel deve ser um interiro")
        classes = []
        for classe in self.__classes:
            if classe.nivel == nivel:
                classes.append(classe)
        return classes

    def get_classe_superior(self, tipo: str, nivel: int):
        """
        Retorna uma classe do mesmo tipo, mas com nivel maior
        :param tipo: tipos de classe como mago, guerreiro, ladino
        :return: classe do nivel acima do anterior
        """
        # Nivel maximo
        if nivel > 3:
            nivel = 3
        if not isinstance(tipo, str):
            raise TypeError("tipo deve ser uma string")
        if not isinstance(nivel, int):
            raise TypeError("nivel deve ser um inteiro")

        for classe in self.__classes:
            if classe.nivel == nivel and classe.tipo == tipo:
                return classe

    def classe_estatisticas(self, classe):
        """
        Retorna uma string formatada com os atributos de uma classe
        :param classe: Classe
        :return:
        Classe:
        Vida: 0
        Defesa: 0
        Mana: 0
        Velocidade: 0
        """
        estatisticas = (classe.nome + ": \nVida: " + str(classe.vida) +
                        "\nDefesa: " + str(classe.defesa) +
                        "\nMana: " + str(classe.mana) +
                        "\nVelocidade: " + str(classe.velocidade))
        return estatisticas

    def classes_estatisticas(self, classes):
        """
        Retorna uma string formatada com os atributos de uma classe
        :param classe: Classe
        :return:
        Classe[index]:
        Vida: 0
        Defesa: 0
        Mana: 0
        Velocidade: 0
        -------------------
        Classe[index+1]:
        Vida: 0
        Defesa: 0
        Mana: 0
        Velocidade: 0
        """
        estatisticas = [classe.nome + "[" + str(index) + "]: \nVida: " + str(classe.vida) +
                        "\nDefesa: " + str(classe.defesa) +
                        "\nMana: " + str(classe.mana) +
                        "\nVelocidade: " + str(classe.velocidade)
                        for index, classe in enumerate(classes)]
        return "\n-------------------\n".join(estatisticas)
