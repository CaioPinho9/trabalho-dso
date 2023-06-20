from enum import Enum


class MenuInicial(Enum):
    MOSTRAR_ESTATISTICAS = "MOSTRAR ESTATISTICAS"
    CRIAR_GRUPO = "CRIAR GRUPO"
    MOSTRAR_GRUPO = "MOSTRAR GRUPO"
    PRIMEIRO_COMBATE = "PRIMEIRO COMBATE"
    SEGUNDO_COMBATE = "SEGUNDO COMBATE"
    ULTIMO_COMBATE = "ULTIMO COMBATE"
    COMBATES = [PRIMEIRO_COMBATE, SEGUNDO_COMBATE, ULTIMO_COMBATE]
    SAIR = "SAIR"


class MenuCriacao(Enum):
    NOME = "NOME"
    SELECIONAR_CLASSE = "SELECIONAR CLASSE"
    ESTATISTICAS_CLASSE = "ESTATISTICAS CLASSE"
    SELECIONAR_PODERES = "SELECIONAR PODERES"
    ESTATISTICAS_PODER = "ESTATISTICAS PODER"
    SELECIONAR_PODER = "SELECIONAR PODER"
    ESCOLHIDOS_PODERES = "PODERES ESCOLHIDOS"
    REMOVER_PODER = "REMOVER PODER SELECIONADO"
    CRIAR = "CRIAR PERSONAGEM"
    CONTINUAR = "CONTINUAR"
    SAIR = "SAIR"


class MenuCombate(Enum):
    ESTATISTICAS_ALVO = "ESTATISTICAS ALVOS"
    SELECIONAR_ALVOS = "SELECIONAR ALVOS"
    SELECIONAR_PODER = "SELECIONAR PODER"
    ESTATISTICAS_PODER = "ESTATISTICAS PODER"
    ATRIBUTOS = "ATRIBUTOS"
    STATUS_BATALHA = "STATUS BATALHA"
    USAR_PODER = "USAR PODER"
    CONTINUAR = "CONTINUAR"
    SAIR = "SAIR"
