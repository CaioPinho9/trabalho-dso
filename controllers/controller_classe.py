from dao.classe_dao import ClasseDAO
from models.classe import Classe


class ControllerClasse:
    def __init__(self):
        self.__classe_dao = ClasseDAO()

    def cadastrar(self, nome: str, vida: int, velocidade: int, defesa: int, mana: int, nivel: int, tipo: str = None):
        """
        Registrar uma classe na lista
        :param nome: Nome da classe
        :param vida: Vida máxima
        :param velocidade: Velocidade usada para ordem de combate
        :param defesa: Dificuldade para acertar o personagem
        :param mana: Mana máxima
        :param nivel: Nivel que essa classe pertence
        :param tipo: Qual grupo essa classe pertence, Mago, Guerreiro, Ladino
        """
        classe = Classe(nome, vida, velocidade, defesa, mana, nivel, tipo)

        self.__classe_dao.add(classe)

        return True

    def get_all(self):
        """
        :return: Retorna todas as classes
        """
        return self.__classe_dao.get_all()

    def remover(self, nome: str):
        """
        Remove uma classe da lista de classes.
        :param nome: nome da classe a ser removido.
        :raise NaoEncontradoException: caso não exista uma Classe com o nome passado na lista de classes.
        """
        classe = self.get(nome)

        self.__classe_dao.remove(classe)

        return True

    def remover_all(self):
        self.__classe_dao.clear_file()
        return True

    def get(self, nome: str):
        """
        Obtém uma classe da lista de classes.
        :param nome: nome da Classe a ser encontrado.
        :return: objeto Classe com o mesmo nome, caso encontrado;
        """
        if not isinstance(nome, str):
            raise TypeError("nome deve ser uma string")

        return self.__classe_dao.get(nome)

    def get_por_nivel(self, nivel: int):
        """
        Retorna uma lista com as classes de certo nivel
        :param nivel: numero que determina a força de um classe
        :return: lista de classes do nivel pedido
        """
        if not isinstance(nivel, int):
            raise TypeError("nivel deve ser um interiro")
        classes = []
        for classe in self.__classe_dao.get_all():
            if classe.nivel == nivel:
                classes.append(classe)
        return classes

    def get_classe_superior(self, tipo: str, nivel: int):
        """
        Retorna uma classe do mesmo tipo, mas com nivel maior
        :param nivel: Indica qual o nivel que está sendo buscado
        :param tipo: tipos de classe como mago, guerreiro, ladino
        :return: classe do nivel acima do anterior
        """
        if not isinstance(tipo, str):
            raise TypeError("tipo deve ser uma string")
        if not isinstance(nivel, int):
            raise TypeError("nivel deve ser um inteiro")
        # Nivel maximo
        if nivel > 3:
            nivel = 3

        for classe in self.__classe_dao.get_all():
            if classe.nivel == nivel and classe.tipo == tipo:
                return classe

    @staticmethod
    def nomes(classes: list[Classe]):
        """
        Retorna uma string formatada com os nomes dos classes
        :param classes:
        :return: list[classe.nome]
        """
        if not all(isinstance(classe, Classe) for classe in classes):
            return TypeError("A lista deve conter classes")

        return [classe.nome for classe in classes]

    def estatisticas_string(self, nome: str):
        """
        Formata uma classe em uma string para ser mostrada na tela
        :param nome: Nome da classe que será mostradas
        :return: String formatada com os atributos da classe
        """
        classe = self.get(nome)

        layout = f"{str(classe.nome)}\n"
        layout += f"Vida: {str(classe.vida)}\n"
        layout += f"Defesa: {str(classe.defesa)}\n"
        layout += f"Mana: {str(classe.mana)}\n"
        layout += f"Velocidade: {str(classe.velocidade)}"

        return layout

    def estatisticas_dict(self, nome: str):
        """
        Retorna um dicionário formatado com os atributos de uma classe
        :param nome: Nome da classe que será mostradas
        :return: {"nome": classe.nome, "vida": str(classe.vida), "defesa": str(classe.defesa),
                  "mana": str(classe.mana), "velocidade": str(classe.velocidade)}
        """
        classe = self.get(nome)

        estatisticas = {"nome": classe.nome, "vida": str(classe.vida), "defesa": str(classe.defesa),
                        "mana": str(classe.mana), "velocidade": str(classe.velocidade)}
        return estatisticas
