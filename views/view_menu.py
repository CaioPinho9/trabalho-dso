import PySimpleGUI as sg

from exceptions import exceptions
from utils.opcoes_menus import MenuInicial
from utils.utils import Utils


class ViewMenu:
    def __init__(self):
        self.window = None

    @staticmethod
    def _combates(combates_vencidos):
        layout = []
        if combates_vencidos >= 0:
            layout.append(
                [sg.Button("Combate Inicial", key=MenuInicial.PRIMEIRO_COMBATE, size=(26, 2), enable_events=True)])
        if combates_vencidos >= 1:
            layout.append(
                [sg.Button("Combate Intermediário", key=MenuInicial.SEGUNDO_COMBATE, size=(26, 2), enable_events=True)])
        if combates_vencidos >= 2:
            layout.append(
                [sg.Button("Combate FINAL", key=MenuInicial.ULTIMO_COMBATE, size=(26, 2), enable_events=True)])
        return layout

    def menu_inicial(self, combates_vencidos):
        layout = [
            [sg.Text("Bem vindo ao RPG (Real Programmed Game), você será um grande herói ou um grande fracassado?")],
            [sg.Text("Esse é um jogo que você precisará de muita habilidade (e sorte) para vencer os 3 combates")],
            [sg.Button("Criar grupo de personagens", key=MenuInicial.CRIAR_GRUPO, size=(26, 2), enable_events=True)],
            [sg.Button("Mostrar grupo de personagens", key=MenuInicial.MOSTRAR_GRUPO, size=(26, 2),
                       enable_events=True)],
            [sg.Button("Mostrar estatisticas", key=MenuInicial.MOSTRAR_ESTATISTICAS, size=(26, 2),
                       enable_events=True)],
            [self._combates(combates_vencidos)],
            [sg.Button("Sair", key=MenuInicial.SAIR, size=(13, 2))]
        ]

        self.window = sg.Window("MENU INICIAL", layout)

        escolha = None

        try:
            while True:
                event, valores = self.window.read()

                if event == sg.WINDOW_CLOSED or event == MenuInicial.SAIR:
                    raise exceptions.FecharPrograma("Fechar o app")

                if event == MenuInicial.CRIAR_GRUPO:
                    return event

                if event == MenuInicial.MOSTRAR_GRUPO:
                    return event

                if event == MenuInicial.MOSTRAR_ESTATISTICAS:
                    return event

                if event == MenuInicial.PRIMEIRO_COMBATE:
                    return event

                if event == MenuInicial.SEGUNDO_COMBATE:
                    return event

                if event == MenuInicial.ULTIMO_COMBATE:
                    return event

        finally:
            self.window.close()

    def sair(self):
        layout = [
            [sg.Text("Obrigado por Jogar!")],
            [sg.Text("Trabalho Nota 10")]
        ]

        self.window = sg.Window("", layout)

        while True:
            event, valores = self.window.read()

            if event == sg.WINDOW_CLOSED or event == MenuInicial.SAIR:
                break

        self.window.close()

    def grupo(self, nomes_jogadores, nivel):
        layout = [
            [sg.Text("O grupo é formado por:")]
        ]

        for nome in nomes_jogadores:
            layout.append([sg.Text(f"{nome}, o {Utils.adjetivo(nivel)}")])

        layout.append([sg.Button("Voltar", key=MenuInicial.SAIR, size=(13, 2))])

        self.window = sg.Window("GRUPO", layout)
        try:
            while True:
                event, valores = self.window.read()

                if event == sg.WINDOW_CLOSED:
                    raise exceptions.FecharPrograma("Fechar")

                if event == MenuInicial.SAIR:
                    raise exceptions.VoltarMenu("Voltar")
        finally:
            self.window.close()

    def desistir(self):
        layout = [
            [sg.Text("O grupo fugiu da luta. GAME OVER.")],
            [sg.Button("Continuar", key=MenuInicial.SAIR, size=(13, 2))]
        ]

        self.window = sg.Window("DESISTIR", layout)
        try:
            while True:
                event, valores = self.window.read()

                if event == sg.WINDOW_CLOSED:
                    raise exceptions.FecharPrograma("Fechar")

                if event == MenuInicial.SAIR:
                    return True
        finally:
            self.window.close()

    def estatisticas(self, estatisticas_jogadores):
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

        self.window = sg.Window("ESTATISTICAS", layout)

        try:
            while True:
                event, valores = self.window.read()

                if event == sg.WINDOW_CLOSED:
                    raise exceptions.FecharPrograma("Fechar")

                if event == MenuInicial.SAIR:
                    raise exceptions.VoltarMenu("Voltar")
        finally:
            self.window.close()
