from models.estatisticas import Estatisticas
from models.personagem import Personagem
from models.classe import Classe


class Jogador(Personagem):
    def __init__(self, nome: str, classe: Classe, codigo: int, poderes=None):
        super().__init__(nome, classe, codigo, poderes)
        self.__estatisticas = Estatisticas()

    def recebeu_dano(self, dano: int, ataque: bool):
        """
        Salva as estatisticas de dano e cura recebidos pelo personagem
        :param dano: Valor de dano ou cura recebido
        :param ataque: Se foi um ataque salva como dano, se não como cura
        """
        if not isinstance(dano, int):
            raise TypeError("dano should be an integer")

        if not isinstance(ataque, bool):
            raise TypeError("ataque should be an boolean")

        if ataque:
            self.__estatisticas.recebeu_dano(abs(dano))
        else:
            self.__estatisticas.recebeu_cura(abs(dano))

    def causou_dano(self, dano: int, ataque: bool):
        """
        Salva as estatisticas de dano e cura causados pelo personagem
        :param dano: Valor de dano ou cura causado
        :param ataque: Se foi um ataque salva como dano, se não como cura
        """
        if not isinstance(dano, int):
            raise TypeError("dano should be an integer")

        if not isinstance(ataque, bool):
            raise TypeError("ataque should be an boolean")

        if ataque:
            self.__estatisticas.causou_dano(abs(dano))
        else:
            self.__estatisticas.causou_cura(abs(dano))

    @property
    def estatisticas(self):
        estatisticas = {
            "nome": self.nome,
            "dano_recebido": self.__estatisticas.dano_recebido,
            "dano_causado": self.__estatisticas.dano_causado,
            "cura_recebida": self.__estatisticas.cura_recebida,
            "cura_causada": self.__estatisticas.cura_causada
        }

        return estatisticas
