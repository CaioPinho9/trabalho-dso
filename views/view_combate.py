import PySimpleGUI as sg

from exceptions import exceptions
from utils.opcoes_menus import MenuCombate


class ViewCombate:
    def __init__(self):
        self.window = None

    def _mostrar_turno(self, nome, turno, jogador):
        layout = [
            [sg.Text(f"TURNO {turno}: {'JOGADOR' if jogador else 'NPC'}: {nome}")],
        ]

        return layout

    def escolher_acao(self, nome, turno):
        layout = self._mostrar_turno(nome, turno, True)

        layout += [
            [sg.Button("Usar Poder", size=(25, 2), key=MenuCombate.USAR_PODER),
             sg.Button("Lista Poderes", size=(25, 2), key=MenuCombate.LISTAR_PODERES)],
            [sg.Button("Status Batalha", size=(25, 2), key=MenuCombate.STATUS_BATALHA),
             sg.Button("Atributos", size=(25, 2), key=MenuCombate.ATRIBUTOS)],
            [sg.Button("Desistir", size=(13, 2), key=MenuCombate.SAIR)]
        ]
        self.window = sg.Window("COMBATE", layout)

        try:
            while True:
                event, valores = self.window.read()

                if event == sg.WINDOW_CLOSED or event == MenuCombate.SAIR:
                    raise exceptions.CombateAcabouException("Voltar para o menu")

                if event == MenuCombate.USAR_PODER:
                    return event

                if event == MenuCombate.LISTAR_PODERES:
                    return event

                if event == MenuCombate.STATUS_BATALHA:
                    return event

                if event == MenuCombate.ATRIBUTOS:
                    return event

        finally:
            self.window.close()

    def escolher_poder(self, nome_personagem, opcoes_poderes, mana):
        print(f"--------------------------------------------------------------------------")
        print(f"O personagem {nome_personagem} tem {mana} de mana sobrando e pode usar esses poderes:\n" +
              opcoes_poderes + "\n")
        print(f"--------------------------------------------------------------------------")
        return input()

    def poder_escolhido(self, poder_nome, ataque, alvos):
        print(f"--------------------------------------------------------------------------")
        print(f"O poder {poder_nome} pode {ataque} {alvos}")

    def escolher_alvos(self, opcoes_alvos, area):
        print(f"--------------------------------------------------------------------------")
        return input(f"Selecione um alvo:\n{opcoes_alvos}\n{area}")

    def iniciar_combate(self, jogadores, npcs):
        layout = [
            [sg.Text("Nesse combate os seguintes personagens se enfrentarão!")],
            [sg.Text("Quem será o vencedor dessa batalha sangrenta!?")],
            [sg.Listbox(jogadores, size=(15, len(jogadores)), disabled=True, no_scrollbar=True), sg.Text("vs"),
             sg.Listbox(npcs, size=(15, len(npcs)), disabled=True, no_scrollbar=True)],
            [sg.Button("Voltar", key=MenuCombate.SAIR), sg.Button("Continuar", key=MenuCombate.CONTINUAR)]
        ]
        self.window = sg.Window("COMBATE", layout)

        try:
            while True:
                event, valores = self.window.read()

                if event == sg.WINDOW_CLOSED or event == MenuCombate.SAIR:
                    raise exceptions.CombateAcabouException("Voltar para o menu")

                if event == MenuCombate.CONTINUAR:
                    return True

        finally:
            self.window.close()

    def resultado_ordem_de_batalha(self, ordem, ordem_nomes):
        layout = [
            [sg.Text(self._resultado_velocidade(ordem))],
            [sg.Text("A ordem de batalha será:")],
            [sg.Listbox(ordem_nomes, size=(15, len(ordem_nomes)), disabled=True, no_scrollbar=True)],
            [sg.Button("Voltar", key=MenuCombate.SAIR), sg.Button("Continuar", key=MenuCombate.CONTINUAR)]
        ]
        self.window = sg.Window("COMBATE", layout)

        try:
            while True:
                event, valores = self.window.read()

                if event == sg.WINDOW_CLOSED or event == MenuCombate.SAIR:
                    return None

                if event == MenuCombate.CONTINUAR:
                    return True

        finally:
            self.window.close()

    def resultado_poder_sucesso(self, poder, dado, acerto, resultado, dano, alvo_nome, alvo_defesa):
        print(f"--------------------------------------------------------------------------")
        print(f"Rolagem [{dado}]+{acerto} = {resultado}, Defesa: {alvo_defesa}")
        print(f"{poder} foi eficaz! Conseguiu causar {dano} de dano em {alvo_nome}!")

    def resultado_poder_falha(self, poder, dado, acerto, resultado, alvo_nome, alvo_defesa):
        print(f"--------------------------------------------------------------------------")
        print(f"Rolagem [{dado}]+{acerto} = {resultado}, Defesa: {alvo_defesa}")
        print(f"{poder} errou {alvo_nome}! ")

    def resultado_cura(self, poder, dano, alvo_nome):
        print(f"--------------------------------------------------------------------------")
        print(f"{poder} foi eficaz! Conseguiu curar {dano} ponto de vida em {alvo_nome}!")

    def escolha_npc(self, nome, poder, alvos):
        print(f"NPC {nome} irá usar {poder} em {alvos}")

    def _mostrar_vida_mana(self, personagem):
        vida_mana = f"{personagem['nome']}: "
        vida_mana += f"HP[{personagem['vida_atual']}/{personagem['vida_maxima']}] "
        vida_mana += f"Mana:[{personagem['mana_atual']}/{personagem['mana_maxima']}]"
        return vida_mana

    def estatistica_vida_mana_geral(self, jogadores, npcs):
        column_jogador = [[sg.Text("Jogadores")]]
        for personagem in jogadores:
            column_jogador.append([sg.Text(self._mostrar_vida_mana(personagem))])

        column_npc = [[sg.Text("Npcs")]]
        for personagem in npcs:
            column_npc.append([sg.Text(self._mostrar_vida_mana(personagem))])

        layout = [
            [sg.Text("STATUS BATALHA")],
            [sg.Column(column_jogador), sg.Column(column_npc)],
            [sg.Button("Voltar", key=MenuCombate.SAIR)]
        ]
        self.window = sg.Window("COMBATE", layout)

        try:
            while True:
                event, valores = self.window.read()

                if event == sg.WINDOW_CLOSED or event == MenuCombate.SAIR:
                    return True

        finally:
            self.window.close()

    def vitoria(self):
        print(f"--------------------------------------------------------------------------")
        print("Parabéns! Vocês venceram essa batalha")
        print(f"--------------------------------------------------------------------------")

    def derrota(self):
        print(f"--------------------------------------------------------------------------")
        print("GAME OVER.")
        print(f"--------------------------------------------------------------------------")

    def estatistica_classe(self, personagem, classe):
        layout = [
            [sg.Text(f"Atributos de {personagem['nome']}")],
            [sg.Text(f"Vida: {personagem['vida_atual']}/{classe['vida']}")],
            [sg.Text(f"Mana: {personagem['mana_atual']}/{classe['mana']}")],
            [sg.Text(f"Defesa: {classe['defesa']}")],
            [sg.Text(f"Velocidade: {classe['velocidade']}")],
            [sg.Button("Voltar", key=MenuCombate.SAIR)]
        ]
        self.window = sg.Window("COMBATE", layout)

        try:
            while True:
                event, valores = self.window.read()

                if event == sg.WINDOW_CLOSED or event == MenuCombate.SAIR:
                    return True

        finally:
            self.window.close()

    def poder_estatistica(self, poderes):
        print(f"--------------------------------------------------------------------------")
        print(poderes)

    def desmaiou(self, nome):
        print(f"--------------------------------------------------------------------------")
        print(f"{nome} desmaiou em combate")

    def _resultado_velocidade(self, ordem):
        layout = ""
        for index, personagem in enumerate(ordem):
            layout += f"{'JOGADOR: ' if personagem['jogador'] else 'NPC: '}"
            layout += f"{personagem['nome']}: "
            layout += f"dado[{personagem['dado']}]"
            layout += f"{'+' if personagem['velocidade'] > 0 else ''}"
            layout += f"{personagem['velocidade']} = {personagem['resultado']}"
            if index != len(ordem) - 1:
                layout += "\n\n"

        return layout
