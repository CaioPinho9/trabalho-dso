class Classe:
    def __init__(self, nome: str, vida: float, velocidade: int, defesa: float, mana: int):
        self.__nome = nome
        self.__vida = vida
        self.__velocidade = velocidade
        self.__defesa = defesa
        self.__mana = mana

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
