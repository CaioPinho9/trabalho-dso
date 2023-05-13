from exceptions.exceptions import DuplicadoException, NaoEncontradoException
from models.poder import Poder


class ControllerPoder:
    def __init__(self):
        self.__poderes = []

    def cadastrar_poder(self, nome: str, acerto: int, dano: int, mana_gasta: int, alvos: int, ataque: bool, nivel: int):
        poder = Poder(nome, acerto, dano, mana_gasta, alvos, ataque, nivel)

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

    @property
    def poderes(self):
        return self.__poderes

    def poderes_por_nivel(self, nivel):
        poderes = []
        for poder in self.__poderes:
            if poder.nivel == nivel:
                poderes.append(poder)
        return poderes

    def poderes_estatisticas(self, poderes):
        poderes_estatisticas = []
        for index, poder in enumerate(poderes):
            estatisticas = poder.nome + "[" + str(index) + "]: "
            estatisticas += "\n[Ataque]" if poder.ataque else "\n[Cura]"
            estatisticas += "\nAcerto: +" + str(poder.acerto) if poder.acerto > 0 else "\nAcerto: " + str(poder.acerto)
            estatisticas += (
                    "\nDano: " + str(poder.dano) +
                    "\nMana Gasta: " + str(poder.mana_gasta) +
                    "\nAlvos: " + str(poder.alvos)
            )
            poderes_estatisticas.append(
                estatisticas
            )

        return "\n-------------------\n".join(poderes_estatisticas)

    def poderes_nomes(self, poderes):
        nomes = [poder.nome for poder in poderes]
        return ", ".join(nomes)
