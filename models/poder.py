class Poder:
    def __init__(self, nome, acerto, dano, mana_gasta, alvos, ataque_cura):
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
