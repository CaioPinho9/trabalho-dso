class Poder:
    def __init__(self, nome: str, acerto: int, dano: int, mana_gasta: int, alvos: int, ataque: bool, nivel: int):
        if not isinstance(nome, str):
            raise TypeError("nome deve ser uma string")
        if not isinstance(acerto, int):
            raise TypeError("acerto deve ser um int")
        if not isinstance(dano, int):
            raise TypeError("dano deve ser um str")
        if not isinstance(mana_gasta, int):
            raise TypeError("mana_gasta deve ser um int")
        if not isinstance(alvos, int):
            raise TypeError("alvos deve ser um int")
        if not isinstance(ataque, bool):
            raise TypeError("ataque_cura deve ser um boolean")
        if not isinstance(nivel, int):
            raise TypeError("nivel deve ser um int")

        self.__nome = nome
        self.__acerto = acerto
        self.__dano = dano
        self.__mana_gasta = mana_gasta
        self.__alvos = alvos
        # Ataque == True, cura == False
        self.__ataque = ataque
        self.__nivel = nivel

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
    def ataque(self):
        return self.__ataque

    @property
    def nivel(self):
        return self.__nivel
