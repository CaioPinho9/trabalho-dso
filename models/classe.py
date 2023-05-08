class Classe:
    def __init__(self, nome: str, vida: int, velocidade: int, defesa: int, mana: int):
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
