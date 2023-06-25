import PySimpleGUI as sg

from exceptions import exceptions
from utils.opcoes_menus import MenuInicial
from utils.utils import adjetivo


class ViewMenu:
    def __init__(self):
        self.__window = None

    @staticmethod
    def _combates(nivel):
        """
        :param nivel: Nivel atual dos jogadores
        :return: Retorna uma lista com os combates disponiveis nesse nivel
        """
        layout = []
        if nivel >= 1:
            layout.append(
                [sg.Button("Combate Inicial", key=MenuInicial.PRIMEIRO_COMBATE, size=(52, 2), enable_events=True)])
        if nivel >= 2:
            layout.append(
                [sg.Button("Combate Intermediário", key=MenuInicial.SEGUNDO_COMBATE, size=(52, 2), enable_events=True)])
        if nivel >= 3:
            layout.append(
                [sg.Button("Combate FINAL", key=MenuInicial.ULTIMO_COMBATE, size=(52, 2), enable_events=True)])
        return layout

    def menu_inicial(self, nivel):
        """
        Tela inicial do jogo
        :param nivel: Nivel atual dos personagens, define quais combates estão disponiveis
        """
        layout = [
            [sg.Text("Bem vindo ao RPG (Real Programmed Game), você será um grande herói ou um grande fracassado?")],
            [sg.Text("Esse é um jogo que você precisará de muita habilidade (e sorte) para vencer os 3 combates")],
            [sg.Button("Criar grupo de personagens", key=MenuInicial.CRIAR_GRUPO, size=(52, 2), enable_events=True)],
            [sg.Button("Mostrar grupo de personagens", key=MenuInicial.MOSTRAR_GRUPO, size=(52, 2),
                       enable_events=True)],
            [sg.Button("Mostrar estatisticas", key=MenuInicial.MOSTRAR_ESTATISTICAS, size=(52, 2),
                       enable_events=True)],
            self._combates(nivel),
            [sg.Button("Resetar", key=MenuInicial.RESETAR_DATABASE, size=(52, 2),
                       enable_events=True)],
            [sg.Button("Sair", key=MenuInicial.SAIR, size=(26, 2))]
        ]

        self.__window = sg.Window("MENU INICIAL", layout, element_justification='center')

        escolha = None

        try:
            while True:
                event, valores = self.__window.read()

                if event == sg.WINDOW_CLOSED or event == MenuInicial.SAIR:
                    raise exceptions.FecharPrograma("Fechar o app")

                if event.value in MenuInicial.BOTOES_MENU_INICIAL.value:
                    return event

        finally:
            self.__window.close()

    def sair(self):
        """
        Tela final ao clicar para sair ou fechar o programa
        Objetivo: Pedir nota por ser engraçado
        """
        layout = [
            [sg.Text("Obrigado por Jogar!")],
            [sg.Text("Trabalho Nota 10")]
        ]

        self.__window = sg.Window("", layout)

        while True:
            event, valores = self.__window.read()

            if event == sg.WINDOW_CLOSED or event == MenuInicial.SAIR:
                break

        self.__window.close()

    def grupo(self, nomes_jogadores: list[str], estatisticas_classes: list[dict],
              nomes_poderes_jogadores: list[list[str]], nivel: int):
        """
        Mostra os Jogadores existentes e seus atributos e poderes
        :param nomes_jogadores: Lista com o nome dos jogadores
        :param estatisticas_classes: Lista com os atributos de cada classe
        :param nomes_poderes_jogadores: Lista com o nome dos poderes de cada jogador
        :param nivel: Nivel de todos os jogadores
        """
        layout = [
            [sg.Text("O grupo é formado por:")]
        ]

        columns = []
        for index, nome_personagem in enumerate(nomes_jogadores):
            estatisticas_classe = estatisticas_classes[index]
            nomes_poderes = nomes_poderes_jogadores[index]
            column = [
                [sg.Text(f"{nome_personagem}, o {adjetivo(nivel)}", background_color=sg.theme_button_color()[1])],
                [sg.Text(f"{estatisticas_classe['nome']}", background_color=sg.theme_button_color()[1])],
                [sg.Text(f"Vida: {estatisticas_classe['vida']}",
                         background_color=sg.theme_button_color()[1])],
                [sg.Text(f"Mana: {estatisticas_classe['mana']}",
                         background_color=sg.theme_button_color()[1])],
                [sg.Text(f"Defesa: {estatisticas_classe['defesa']}", background_color=sg.theme_button_color()[1])],
                [sg.Text(f"Velocidade: {estatisticas_classe['velocidade']}",
                         background_color=sg.theme_button_color()[1])],
                [sg.Text("Poderes:",
                         background_color=sg.theme_button_color()[1])],
                [sg.Listbox(nomes_poderes, disabled=True, no_scrollbar=True, size=(23, len(nomes_poderes)))]
            ]
            columns.append(sg.Column(column, background_color=sg.theme_button_color()[1]))

        layout.append(columns)
        layout.append([sg.Button("Voltar", key=MenuInicial.SAIR, size=(13, 2))])

        self.__window = sg.Window("GRUPO", layout, element_justification='center')
        try:
            while True:
                event, valores = self.__window.read()

                if event == sg.WINDOW_CLOSED:
                    raise exceptions.FecharPrograma("Fechar")

                if event == MenuInicial.SAIR:
                    raise exceptions.VoltarMenu("Voltar")
        finally:
            self.__window.close()

    def estatisticas(self, estatisticas_jogadores):
        """
        Tela que mostra quais atributos e poderes cada jogador possui
        :param estatisticas_jogadores:
        """
        layout = [
            [sg.Text("O grupo possui as seguintes estátisticas:")],
        ]

        columns = []
        for estatistica_jogador in estatisticas_jogadores:
            column = [[sg.Text(f"{estatistica_jogador['nome']}", background_color=sg.theme_button_color()[1])],
                      [sg.Text(f"Dano causado: {estatistica_jogador['dano_causado']}",
                               background_color=sg.theme_button_color()[1])],
                      [sg.Text(f"Cura causada: {estatistica_jogador['cura_causada']}",
                               background_color=sg.theme_button_color()[1])],
                      [sg.Text(f"Dano recebido: {estatistica_jogador['dano_recebido']}",
                               background_color=sg.theme_button_color()[1])],
                      [sg.Text(f"Cura recebida: {estatistica_jogador['cura_recebida']}",
                               background_color=sg.theme_button_color()[1])]]
            columns.append(sg.Column(column, background_color=sg.theme_button_color()[1]))

        layout.append(columns)

        layout.append([sg.Button("Voltar", key=MenuInicial.SAIR, size=(13, 2))])

        self.__window = sg.Window("ESTATISTICAS", layout, element_justification='center')

        try:
            while True:
                event, valores = self.__window.read()

                if event == sg.WINDOW_CLOSED:
                    raise exceptions.FecharPrograma("Fechar")

                if event == MenuInicial.SAIR:
                    raise exceptions.VoltarMenu("Voltar")
        finally:
            self.__window.close()

    def resetar_database(self):
        """
        Tela para confirmar se deseja resetar o programa
        """
        layout = [
            [sg.Text("Deseja resetar mesmo? Você perderá todo o progresso!")],
            [sg.Button("Voltar", key=MenuInicial.SAIR, size=(13, 2)),
             sg.Button("Confirmar", key=MenuInicial.RESETAR_DATABASE, size=(13, 2))]
        ]

        self.__window = sg.Window("RESETAR", layout, element_justification='center')

        try:
            while True:
                event, valores = self.__window.read()

                if event == sg.WINDOW_CLOSED:
                    raise exceptions.FecharPrograma("Fechar")

                if event == MenuInicial.SAIR:
                    raise exceptions.VoltarMenu("Voltar")

                if event == MenuInicial.RESETAR_DATABASE:
                    return True

        finally:
            self.__window.close()
