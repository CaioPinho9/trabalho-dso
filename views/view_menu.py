import PySimpleGUI as sg

from utils.menu_enum import Opcao


class ViewMenu:
    def __init__(self):
        self.window = None

    @staticmethod
    def _combates(combates_vencidos):
        layout = []
        if combates_vencidos >= 0:
            layout.append([sg.Button("Combate Inicial", key=Opcao.PRIMEIRO_COMBATE, size=(25, 2), enable_events=True)])
        if combates_vencidos >= 1:
            layout.append(
                [sg.Button("Combate Intermediário", key=Opcao.SEGUNDO_COMBATE, size=(25, 2), enable_events=True)])
        if combates_vencidos >= 2:
            layout.append([sg.Button("Combate FINAL", key=Opcao.ULTIMO_COMBATE, size=(25, 2), enable_events=True)])
        return layout

    def menu_inicial(self, combates_vencidos):
        layout = [
            [sg.Text("Bem vindo ao RPG (Real Programmed Game), você será um grande herói ou um grande fracassado?")],
            [sg.Text("Esse é um jogo que você precisará de muita habilidade (e sorte) para vencer os 3 combates")],
            [sg.Button("Criar grupo de personagens", key=Opcao.CRIAR_GRUPO, size=(25, 2), enable_events=True)],
            [sg.Button("Mostrar grupo de personagens", key=Opcao.MOSTRAR_GRUPO, size=(25, 2), enable_events=True)],
            [self._combates(combates_vencidos)],
            [sg.Button("Sair", key="-EXIT-", size=(12, 2))]
        ]

        self.window = sg.Window("MENU INICIAL", layout)

        escolha = None

        while True:
            event, valores = self.window.read()

            if event == sg.WINDOW_CLOSED or event == "-EXIT-":
                break

            if event == Opcao.CRIAR_GRUPO:
                escolha = event
                break
            if event == Opcao.MOSTRAR_GRUPO:
                escolha = event
                break
            if event == Opcao.PRIMEIRO_COMBATE:
                escolha = event
                break
            if event == Opcao.SEGUNDO_COMBATE:
                escolha = event
                break
            if event == Opcao.ULTIMO_COMBATE:
                escolha = event
                break

        self.window.close()
        return escolha

    def sair(self):
        layout = [
            [sg.Text("Obrigado por Jogar!")],
            [sg.Text("Trabalho Nota 10")]
        ]

        self.window = sg.Window("", layout)

        while True:
            event, valores = self.window.read()

            if event == sg.WINDOW_CLOSED or event == "-EXIT-":
                break

        self.window.close()

    def grupo(self, grupo):
        print(f"--------------------------------------------------------------------------")
        print(f"O grupo é formado pelo {grupo}")

    def desistir(self):
        print(f"--------------------------------------------------------------------------")
        print("O grupo fugiu da luta. GAME OVER.")
        print(f"--------------------------------------------------------------------------")
