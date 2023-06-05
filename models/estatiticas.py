class Estatisticas:
    def __init__(self):
        self.__dano_recebido = 0
        self.__dano_causado = 0
        self.__cura_recebida = 0
        self.__cura_causada = 0

    def causou_dano(self, dano):
        self.__dano_causado += dano

    def recebeu_dano(self, dano):
        self.__dano_recebido += dano

    def causou_cura(self, cura):
        self.__cura_causada += cura

    def recebeu_cura(self, cura):
        self.__cura_recebida += cura

    @property
    def dano_causado(self):
        return self.__dano_causado

    @property
    def dano_recebido(self):
        return self.__dano_recebido

    @property
    def cura_causada(self):
        return self.__cura_causada

    @property
    def cura_recebida(self):
        return self.__cura_recebida
