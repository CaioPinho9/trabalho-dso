class Poder:
    def __init__(self, nome: str, acerto: float, dano: float, mana_gasta: int, alvos: int, ataque_cura: bool):
        if not isinstance(nome, str):
            raise TypeError("nome deve ser uma string")
        if not isinstance(acerto, str):
            raise TypeError("acerto deve ser um float")
        if not isinstance(dano, str):
            raise TypeError("dano deve ser um float")
        if not isinstance(mana_gasta, str):
            raise TypeError("mana_gasta deve ser um int")
        if not isinstance(alvos, str):
            raise TypeError("alvos deve ser um int")
        if not isinstance(ataque_cura, bool):
            raise TypeError("ataque_cura deve ser um boolean")

        self.__nome = nome
        self.__acerto = acerto,
        self.__dano = dano
        self.__mana_gasta = mana_gasta
        self.__alvos = alvos
        self.__ataque_cura = ataque_cura

    @property
    def nome(self):
        return self.__nome

    @property
    def acerto(self):
        return self.__acerto

    @property
    def dano(self):
        return self.__dano

    @property
    def mana_gasta(self):
        return self.__mana_gasta

    @property
    def alvos(self):
        return self.__alvos

    @property
    def ataque_cura(self):
        return self.__ataque_cura
