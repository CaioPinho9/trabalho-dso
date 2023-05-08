class Item:
    def __init__(self, nome, buff_ataque, buff_defesa, buff_acerto):
        if not isinstance(nome, str):
            raise TypeError("Nome do item deve ser do tipo string")
        if not isinstance(buff_ataque, int):
            raise TypeError("Buff de ataque do item deve ser do tipo inteiro")
        if not isinstance(buff_defesa, int):
            raise TypeError("Buff de defesa do item deve ser do tipo inteiro")
        if not isinstance(buff_acerto, int):
            raise TypeError("Buff de acerto do item deve ser do tipo inteiro")

        self.__nome = nome
        self.__buff_ataque = buff_ataque
        self.__buff_defesa = buff_defesa
        self.__buff_acerto = buff_acerto
        self.__utilizado = False
    
    @property
    def nome(self):
        return self.__nome
    
    @property
    def buff_ataque(self):
        return self.__buff_ataque
    
    @property
    def buff_defesa(self):
        return self.__buff_defesa
    
    @property
    def buff_acerto(self):
        return self.__buff_acerto
    
    @property
    def utilizado(self):
        return self.__utilizado

    @utilizado.setter
    def utilizado(self, valor):
        if not isinstance(valor, bool):
            raise TypeError("Utilizado deve ser do tipo booleano")
        self.__utilizado = valor
