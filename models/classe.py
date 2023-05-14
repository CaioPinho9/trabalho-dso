class Classe:
    def __init__(self, nome: str, vida: int, velocidade: int, defesa: int, mana: int, nivel: int, tipo: str = None):
        if not isinstance(nome, str):
            raise TypeError("nome deve ser um str")
        if not isinstance(vida, int):
            raise TypeError("vida deve ser um int")
        if not isinstance(velocidade, int):
            raise TypeError("velocidade deve ser um int")
        if not isinstance(defesa, int):
            raise TypeError("defesa deve ser um int")
        if not isinstance(mana, int):
            raise TypeError("mana deve ser um int")
        if not isinstance(nivel, int):
            raise TypeError("nivel deve ser um int")
        if not isinstance(tipo, str) and tipo:
            raise TypeError("tipo deve ser uma str")

        self.__nome = nome
        self.__vida = vida
        self.__velocidade = velocidade
        self.__defesa = defesa
        self.__mana = mana
        self.__nivel = nivel
        self.__tipo = tipo

    @property
    def nome(self):
        return self.__nome

    @property
    def vida(self):
        return self.__vida

    @property
    def velocidade(self):
        return self.__velocidade

    @property
    def defesa(self):
        return self.__defesa

    @property
    def mana(self):
        return self.__mana

    @property
    def nivel(self):
        return self.__nivel

    @property
    def tipo(self):
        return self.__tipo
