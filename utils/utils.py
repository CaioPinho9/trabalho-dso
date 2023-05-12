from views.view_combate import ViewCombate


class Utils:
    @staticmethod
    def check_inteiro_intervalo(valor: int, intervalo: list[int, int]):
        try:
            if not intervalo[0] <= int(valor) <= intervalo[1]:
                raise TypeError("Deve ser um dos números da lista")
            return True
        except Exception:
            return False
