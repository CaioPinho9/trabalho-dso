from exceptions import exceptions
from models.poder import Poder


class ControllerPoder:
    def __init__(self):
        self.__poderes = []

    def cadastrar_poder(self, nome: str, acerto: int, dano: int, mana_gasta: int, alvos: int, ataque: bool, nivel: int):
        """
        Cadastrar um poder
        :param nome: nome do poder
        :param acerto: aumenta a chance de acerto
        :param dano: valor usado para alterar a vida
        :param mana_gasta: valor gasto ao usar o poder
        :param alvos: personagens que serão acertados
        :param ataque: se o ataque causa dano ou cura o alvo
        :param nivel: valor que indica o quao forte é o poder
        :raise DuplicadoException: Se um poder com esse nome já existir
        :return: poder
        """
        poder = Poder(nome, acerto, dano, mana_gasta, alvos, ataque, nivel)

        if self.get_poder(poder.nome):
            raise exceptions.DuplicadoException('Não foi possivel criar o poder pois ja existe um com o mesmo nome')

        self.__poderes.append(poder)

        return poder

    def remover_poder(self, nome: str):
        """
        Remove um objeto Poder da lista de poderes.
        :param nome: nome do objeto Poder a ser removido.
        :raise NaoEncontradoException: caso não exista um objeto Poder com o nome passado na lista de poderes.
        :return: True
        """
        poder = self.get_poder(nome)
        if not poder:
            raise exceptions.NaoEncontradoException("O poder não foi encontrado.")

        self.__poderes.remove(poder)

        return True

    def get_poder(self, nome: str):
        """
        Obtém um objeto Poder da lista de poderes.
        :param nome: (str) nome do objeto Poder a ser encontrado.
        :return: Poder: objeto Poder com o mesmo nome, caso encontrado; ou None, caso não encontrado.
        """
        for poder in self.__poderes:
            if poder.nome == nome:
                return poder
        return None

    @property
    def poderes(self):
        return self.__poderes

    def get_poderes_por_nivel(self, nivel):
        """
        Retorna uma lista com os poderes de certo nivel
        :param nivel: numero que determina a força de um poder
        :return: lista de poderes do nivel pedido
        """
        poderes = []
        for poder in self.__poderes:
            if poder.nivel == nivel:
                poderes.append(poder)
        return poderes

    def get_poderes_ate_nivel(self, nivel):
        """
        Retorna uma lista com os poderes até certo nivel
        :param nivel: numero que determina a força de um poder
        :return: lista de poderes do nivel pedido
        """
        poderes = []
        for poder in self.__poderes:
            if poder.nivel <= nivel:
                poderes.append(poder)
        return poderes

    def poderes_estatisticas(self, poderes: list[Poder]):
        """
        Retorna uma string formatada com os atributos dos poderes
        :param poderes: list[Poder]
        :return:
        Poder[index]:
        [Ataque]
        Acerto: +acerto
        Dano: dano
        Mana Gasta: mana_gasta
        Alvos: alvos
        -------------------
        Poder[index + 1]:
        [Ataque]
        Acerto: +acerto
        Dano: dano
        Mana Gasta: mana_gasta
        Alvos: alvos
        """
        poderes_estatisticas = []
        for index, poder in enumerate(poderes):
            estatisticas = poder.nome + "[" + str(index) + "]: "
            estatisticas += "\n[Ataque]" if poder.ataque else "\n[Cura]"
            estatisticas += "\nAcerto: +" + str(poder.acerto) if poder.acerto > 0 else "\nAcerto: " + str(poder.acerto)
            estatisticas += "\nDano: " + str(poder.dano) if poder.ataque else "\nCura: " + str(poder.dano)
            estatisticas += "\nMana Gasta: " + str(poder.mana_gasta)
            estatisticas += "\nAlvos: " + str(poder.alvos)

            poderes_estatisticas.append(
                estatisticas
            )

        return "\n-------------------\n".join(poderes_estatisticas)

    def nomes(self, poderes: list[Poder]):
        """
        Retorna uma string formatada com os nomes dos poderes
        :param poderes:
        :return: list[poder.nome]
        """
        if not all(isinstance(poder, Poder) for poder in poderes):
            return TypeError("A lista deve conter personagens")

        return [poder.nome for poder in poderes]

    def estatisticas(self, poder_name: str):
        poder = self.get_poder(poder_name)

        if not poder:
            raise exceptions.NaoEncontradoException("Poder não encontrado")

        layout = f"[{poder.nome} Nvl{poder.nivel}]\n"
        layout += f"{'Dano' if poder.ataque else 'Cura'}: {poder.dano}\n"
        layout += f"Acerto: {poder.acerto}\n"
        layout += f"Mana: {poder.mana_gasta}\n"
        layout += f"Acerta {poder.alvos} {'alvo' if poder.alvos == 1 else 'alvos'}"
        return layout
