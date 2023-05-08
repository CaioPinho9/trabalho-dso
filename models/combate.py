from models.jogador import Jogador
from models.npc import Npc

class Combate():
    def __init__(self, codigo: str, jogadores: list[Jogador], inimigos: list[Npc]):
        if not isinstance(codigo, str):
            raise TypeError("Código do combate deve ser do tipo string")
        if not isinstance(jogadores, list):
            raise TypeError("Jogadores do combate deve ser do tipo lista")
        if not isinstance(inimigos, list):
            raise TypeError("Inimigos do combate deve ser do tipo lista")
        if not all(isinstance(jogador, Jogador) for jogador in jogadores):
            raise TypeError("Jogadores do combate devem ser do tipo Jogador")
        if not all(isinstance(inimigo, Npc) for inimigo in inimigos):
            raise TypeError("Inimigos do combate devem ser do tipo Npc")
        if len(jogadores) == 0:
            raise ValueError("Combate deve ter pelo menos um jogador")
        if len(inimigos) == 0:
            raise ValueError("Combate deve ter pelo menos um inimigo")
        
        self.__codigo = codigo
        self.__inimigos = inimigos
        self.__jogadores = jogadores
        self.__ordem_de_batalha = []
        self.__vitoria = 0
        self.__dano_causado = 0
        self.__dano_recebido = 0
        self.__finalizado = False

    @property
    def codigo(self):
        return self.__codigo
    
    @property
    def jogadores(self):
        return self.__jogadores
    
    @property
    def inimigos(self):
        return self.__inimigos
    
    @property
    def ordem_de_batalha(self):
        return self.__ordem_de_batalha
    
    @property
    def vitoria(self):
        return self.__vitoria

    @property
    def dano_causado(self):
        return self.__dano_causado
    
    @property
    def dano_recebido(self):
        return self.__dano_recebido
    
    @property
    def finalizado(self):
        return self.__finalizado
    
    @jogadores.setter
    def jogadores(self, lista_de_jogadores):
        if not isinstance(lista_de_jogadores, list):
            raise TypeError("Jogadores deve ser do tipo lista")
        if not all(isinstance(jogador, Jogador) for jogador in lista_de_jogadores):
            raise TypeError("Jogadores deve ser do tipo Jogador")
        if len(lista_de_jogadores) == 0:
            raise ValueError("Combate deve ter pelo menos um jogador")
        self.__jogadores = lista_de_jogadores

    @inimigos.setter
    def inimigos(self, lista_de_inimigos):
        if not isinstance(lista_de_inimigos, list):
            raise TypeError("Inimigos deve ser do tipo lista")
        if not all(isinstance(inimigo, Npc) for inimigo in lista_de_inimigos):
            raise TypeError("Inimigos deve ser do tipo Npc")
        if len(lista_de_inimigos) == 0:
            raise ValueError("Combate deve ter pelo menos um inimigo")
        self.__inimigos = lista_de_inimigos

    @ordem_de_batalha.setter
    def ordem_de_batalha(self, lista_de_batalha):
        if not isinstance(lista_de_batalha, list):
            raise TypeError("Ordem de batalha deve ser do tipo lista")
        if not all(isinstance(batalha, Jogador) for batalha in lista_de_batalha):
            raise TypeError("Ordem de batalha deve ser do tipo Jogador")
        self.__ordem_de_batalha = lista_de_batalha
    
    @vitoria.setter
    def vitoria(self, valor):
        if not isinstance(valor, int):
            raise TypeError("Vitoria deve ser do tipo inteiro")
        self.__vitoria = valor
    
    @dano_causado.setter
    def dano_causado(self, valor):
        if not isinstance(valor, int):
            raise TypeError("Dano causado deve ser do tipo inteiro")
        self.__dano_causado = valor
    
    @dano_recebido.setter
    def dano_recebido(self, valor):
        if not isinstance(valor, int):
            raise TypeError("Dano recebido deve ser do tipo inteiro")
        self.__dano_recebido = valor
    
    @finalizado.setter
    def finalizado(self, valor):
        if not isinstance(valor, bool):
            raise TypeError("Finalizado deve ser do tipo booleano")
        self.__finalizado = valor
    
    def adicionar_inimigo(self, inimigo):
        if not isinstance(inimigo, Npc):
            raise TypeError("Inimigo deve ser do tipo Npc")
        self.__inimigos.append(inimigo)
    
    def remover_inimigo(self, inimigo):
        if not isinstance(inimigo, Npc):
            raise TypeError("Inimigo deve ser do tipo Npc")
        self.__inimigos.remove(inimigo)
    
    def proximo_da_batalha(self):
        """
            Adicionar logica de mostrar quando a batalha terminou
        """
        if (len(self.__jogadores <= 0)):
            raise ValueError("Não há jogadores para batalhar")
        if (len(self.__inimigos <= 0)):
            raise ValueError("Não há inimigos para batalhar")
        ordem_encerrada = self.__ordem_de_batalha.pop(0)
        self.__ordem_de_batalha.append(ordem_encerrada)
        proximo_da_batalha = self.__ordem_de_batalha[0]

        return proximo_da_batalha
