from dao.poder_dao import PoderDAO
from models.poder import Poder


class ControllerPoder:
    def __init__(self):
        self.__poder_dao = PoderDAO()

    def cadastrar(self, nome: str, acerto: int, dano: int, mana_gasta: int, alvos: int, ataque: bool, nivel: int):
        """
        Registrar um poder
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

        self.__poder_dao.add(poder)

        return poder

    def remover(self, nome: str):
        """
        Remove um objeto Poder da lista de poderes.
        :param nome: nome do objeto Poder a ser removido.
        :raise NaoEncontradoException: caso não exista um objeto Poder com o nome passado na lista de poderes.
        :return: True
        """

        self.__poder_dao.remove(nome)

        return True

    def remover_all(self):
        """
        Remove todos os poderes da lista
        """
        self.__poder_dao.clear_file()
        return True

    def get(self, nome: str):
        """
        Obtém um objeto Poder da lista de poderes.
        :param nome: (str) nome do objeto Poder a ser encontrado.
        :raise NaoEncontradoException: caso não exista um objeto Poder com o nome passado na lista de poderes.
        :return: Poder: objeto Poder com o mesmo nome, caso encontrado.
        """
        return self.__poder_dao.get(nome)

    def get_all(self):
        """
        :return: Retorna uma lista com todos os poderes
        """
        return self.__poder_dao.get_all()

    def get_ate_nivel(self, nivel):
        """
        Retorna uma lista com os poderes até certo nivel
        :param nivel: numero que determina a força de um poder
        :return: lista de poderes do nivel pedido
        """
        poderes = []
        for poder in self.__poder_dao.get_all():
            if 0 < poder.nivel <= nivel:
                poderes.append(poder)
        return poderes

    def estatistica(self, nome: str):
        """
        Retorna uma string com os atributos de um poder especifico
        :param nome: Nome do poder que será mostrado
        :return: String formatada para visualizar
        """
        poder = self.get(nome)

        layout = f"[{poder.nome} Nvl{poder.nivel}]\n"
        layout += f"{'Dano' if poder.ataque else 'Cura'}: {poder.dano}\n"
        layout += f"Acerto: {poder.acerto}\n"
        layout += f"Mana: {poder.mana_gasta}\n"
        layout += f"Acerta {poder.alvos} {'alvo' if poder.alvos == 1 else 'alvos'}"
        return layout

    @staticmethod
    def estatisticas(poderes: list[Poder]):
        """
        Retorna um dicionário formatado com os atributos dos poderes
        :param poderes: list[Poder]
        :return: {"nome": poder.nome, "ataque": poder.ataque, "acerto": str(poder.acerto),
                  "dano": str(poder.dano), "mana_gasta": str(poder.mana_gasta), "alvos": str(poder.alvos)}
        """
        poderes_dict = []
        for poder in poderes:
            estatisticas = {"nome": poder.nome, "ataque": poder.ataque, "acerto": str(poder.acerto),
                            "dano": str(poder.dano), "mana_gasta": str(poder.mana_gasta), "alvos": str(poder.alvos)}

            poderes_dict.append(estatisticas)

        return poderes_dict

    @staticmethod
    def nomes(poderes: list[Poder]):
        """
        Retorna uma string formatada com os nomes dos poderes
        :param poderes:
        :return: list[poder.nome]
        """
        if not all(isinstance(poder, Poder) for poder in poderes):
            return TypeError("A lista deve conter personagens")

        return [poder.nome for poder in poderes]
