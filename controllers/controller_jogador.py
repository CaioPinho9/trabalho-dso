from models.poder import Poder
class ControllerPoder:
    def __init__(self):
        self.__poderes = []
    
    def cadastrar_poder(self, poder):
        if not isinstance(poder, Poder):
            raise TypeError("Poder inválido")
        if poder.nome in [item.nome for item in self.__poderes]:
            raise ValueError("Poder já cadastrado")
    
    def remover_poder(self, nome):
        for index, poder in enumerate(self.__poderes):
            if poder.nome == nome:
                self.__poderes.pop(index)
    
    def listar_poderes(self):
        return self.__poderes
    