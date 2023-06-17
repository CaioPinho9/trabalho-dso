import random


class Utils:
    @staticmethod
    def check_inteiro_intervalo(valor: int, intervalo: list[int, int]):
        try:
            if not intervalo[0] <= int(valor) <= intervalo[1]:
                raise TypeError("Deve ser um dos números da lista")
            return True
        except ValueError:
            raise TypeError("Precisa ser um inteiro")

    @staticmethod
    def adjetivo(nivel: int):
        if not isinstance(nivel, int):
            raise TypeError("nivel deve ser um inteiro")

        adjetivos = []
        if nivel == 1:
            adjetivos = ["tolo", "fracassado", "idiota", "imbecil", "pateta", "desajeitado", "ingênuo"]
        elif nivel == 2:
            adjetivos = ["medíocre aventureiro", "típico aventureiro", "aventureiro comum", "destemido", "corajoso"]
        elif nivel == 3:
            adjetivos = ["incrível aventureiro", "herói", "excelente aventureiro", "grande aventureiro", "ousado",
                         "intrépido"]
        return random.choice(adjetivos)

    @staticmethod
    def list_to_string(list):
        if len(list) <= 1:
            return ''.join(list)
        else:
            return ', '.join(list[:-1]) + ' e ' + list[-1]
