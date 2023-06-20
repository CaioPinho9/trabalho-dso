from models.estatisticas import Estatisticas
from models.personagem import Personagem
from models.classe import Classe
from models.poder import Poder


class Jogador(Personagem):
    def __init__(self, nome: str, classe: Classe, poderes: list[Poder] = []):
        super().__init__(nome, classe, poderes)
        self.__estatisticas = Estatisticas()

    def recebeu_dano(self, dano):
        self.__estatisticas.recebeu_dano(dano)

    def causou_dano(self, dano):
        self.__estatisticas.causou_dano(dano)

    def recebeu_cura(self, cura):
        self.__estatisticas.recebeu_cura(cura)

    def causou_cura(self, cura):
        self.__estatisticas.causou_cura(cura)

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