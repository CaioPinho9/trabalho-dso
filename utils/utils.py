import random


class Utils:
    @staticmethod
    def adjetivo(nivel: int):
        if not isinstance(nivel, int):
            raise TypeError("nivel deve ser um inteiro")

        adjetivos = []
        if nivel == 1:
            adjetivos = ["tolo", "fracassado", "idiota", "imbecil", "pateta", "desajeitado", "ingênuo"]
        elif nivel == 2:
            adjetivos = ["medíocre aventureiro", "típico aventureiro", "aventureiro comum", "destemido", "corajoso"]
        elif nivel >= 3:
            adjetivos = ["incrível aventureiro", "herói", "excelente aventureiro", "grande aventureiro", "ousado",
                         "intrépido"]
        return random.choice(adjetivos)

    @staticmethod
    def list_to_string(list: list):
        if len(list) <= 1:
            return ''.join(list)
        else:
            return ', '.join(list[:-1]) + ' e ' + list[-1]
