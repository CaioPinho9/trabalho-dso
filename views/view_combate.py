import PySimpleGUI as sg

from exceptions import exceptions
from utils.opcoes_menus import MenuCombate


class ViewCombate:
    def __init__(self, controller_poder):
        self._controller_poder = controller_poder
        self._window = None

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

    def _mostrar_turno(self, nome, turno, jogador):
        layout = [
            [sg.Text(f"TURNO {turno}: {'JOGADOR' if jogador else 'NPC'}: {nome}")],
        ]

        return layout

    def _mostrar_vida_mana(self, personagem):
        vida_mana = f"{personagem['nome']}: "
        vida_mana += f"HP[{personagem['vida_atual']}/{personagem['vida_maxima']}] "
        vida_mana += f"Mana:[{personagem['mana_atual']}/{personagem['mana_maxima']}]"
        return vida_mana

    def _vida_mana_geral(self, personagens, tipo):
        column = [[sg.Text(f"{tipo}:")]]
        for personagem in personagens:
            column.append([sg.Text(self._mostrar_vida_mana(personagem))])

        return column

    def escolher_acao(self, nome, turno):
        layout = self._mostrar_turno(nome, turno, True)

        layout += [
            [sg.Button("Usar Poder", size=(26, 2), key=MenuCombate.USAR_PODER)],
            [sg.Button("Status Batalha", size=(26, 2), key=MenuCombate.STATUS_BATALHA)],
            [sg.Button("Atributos", size=(26, 2), key=MenuCombate.ATRIBUTOS)],
            [sg.Button("Desistir", size=(13, 2), key=MenuCombate.SAIR)]
        ]
        self._window = sg.Window("COMBATE", layout)

        try:
            while True:
                event, valores = self._window.read()

                if event == sg.WINDOW_CLOSED or event == MenuCombate.SAIR:
                    raise exceptions.CombateAcabouException("Voltar para o menu")

                if event == MenuCombate.USAR_PODER:
                    return event

                if event == MenuCombate.STATUS_BATALHA:
                    return event

                if event == MenuCombate.ATRIBUTOS:
                    return event

        finally:
            self._window.close()

    def escolher_poder(self, nome_personagem, turno, poderes_nome, mana):
        layout = self._mostrar_turno(nome_personagem, turno, True)

        layout += [
            [sg.Text(f"O personagem {nome_personagem} tem {mana} de mana sobrando e pode usar esses poderes:")],
            [sg.Listbox(values=poderes_nome, size=(26, 5), enable_events=True, key=MenuCombate.SELECIONAR_PODER,
                        default_values=poderes_nome[0]),
             sg.Text(self._controller_poder.estatisticas(poderes_nome[0]), key=MenuCombate.ESTATISTICAS_PODER,
                     size=(21, 5)),
             sg.Column([[sg.Button("Usar", key=MenuCombate.CONTINUAR, size=(13, 2))],
                        [sg.Button("Voltar", key=MenuCombate.SAIR, size=(13, 2))]])]
        ]

        self._window = sg.Window("COMBATE", layout)

        try:
            while True:
                event, valores = self._window.read()

                if event == sg.WINDOW_CLOSED:
                    raise exceptions.CombateAcabouException("Voltar para o menu")

                if event == MenuCombate.SAIR:
                    return None

                if event == MenuCombate.SELECIONAR_PODER:
                    poder_selecionado = valores[event][0]

                    if poder_selecionado:
                        self._window.Element(MenuCombate.ESTATISTICAS_PODER).update(
                            self._controller_poder.estatisticas(poder_selecionado)
                        )

                if event == MenuCombate.CONTINUAR:
                    return valores[MenuCombate.SELECIONAR_PODER][0]

        finally:
            self._window.close()

    def poder_escolhido(self, poder_nome, ataque, alvos):
        print(f"--------------------------------------------------------------------------")
        print(f"O poder {poder_nome} pode {ataque} {alvos}")

    def escolher_alvos(self, poder_dict, alvos_disponiveis, alvos_maximos, jogador):
        efeito = "acertar" if poder_dict['ataque'] else "curar"
        efeito += " até" if alvos_maximos > 0 else ""

        layout = [
            [sg.Text(f"O poder {poder_dict['nome']} pode {efeito} {poder_dict['alvos']} alvos")],
            [sg.Listbox(alvos_disponiveis, size=(15, len(alvos_disponiveis)), no_scrollbar=True,
                        key=MenuCombate.SELECIONAR_ALVOS, enable_events=True,
                        select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE)],
            [sg.Button("Voltar", key=MenuCombate.SAIR, size=(13, 2)),
             sg.Button("Continuar", key=MenuCombate.CONTINUAR, size=(13, 2))]
        ]
        self._window = sg.Window("COMBATE", layout)

        try:
            while True:
                event, valores = self._window.read()

                if event == sg.WINDOW_CLOSED or event == MenuCombate.SAIR:
                    return

                if event == MenuCombate.CONTINUAR:
                    alvos_selecionados = valores[MenuCombate.SELECIONAR_ALVOS]
                    if len(alvos_selecionados) == alvos_maximos:
                        return alvos_selecionados
                    sg.popup_error(f"Escolha {alvos_maximos} alvos.")


        finally:
            self._window.close()

    def iniciar_combate(self, jogadores, npcs):
        layout = [
            [sg.Text("Nesse combate os seguintes personagens se enfrentarão!")],
            [sg.Text("Quem será o vencedor dessa batalha sangrenta!?")],
            [sg.Listbox(jogadores, size=(15, len(jogadores)), disabled=True, no_scrollbar=True), sg.Text("vs"),
             sg.Listbox(npcs, size=(15, len(npcs)), disabled=True, no_scrollbar=True)],
            [sg.Button("Desistir", key=MenuCombate.SAIR, size=(13, 2)),
             sg.Button("Continuar", key=MenuCombate.CONTINUAR, size=(13, 2))]
        ]
        self._window = sg.Window("COMBATE", layout)

        try:
            while True:
                event, valores = self._window.read()

                if event == sg.WINDOW_CLOSED or event == MenuCombate.SAIR:
                    raise exceptions.CombateAcabouException("Voltar para o menu")

                if event == MenuCombate.CONTINUAR:
                    return True

        finally:
            self._window.close()

    def resultado_ordem_de_batalha(self, ordem, ordem_nomes):
        layout = [
            [sg.Text(self._resultado_velocidade(ordem))],
            [sg.Text("A ordem de batalha será:")],
            [sg.Listbox(ordem_nomes, size=(15, len(ordem_nomes)), disabled=True, no_scrollbar=True)],
            [sg.Button("Desistir", key=MenuCombate.SAIR, size=(13, 2)),
             sg.Button("Continuar", key=MenuCombate.CONTINUAR, size=(13, 2))]
        ]
        self._window = sg.Window("COMBATE", layout)

        try:
            while True:
                event, valores = self._window.read()

                if event == sg.WINDOW_CLOSED or event == MenuCombate.SAIR:
                    return None

                if event == MenuCombate.CONTINUAR:
                    return True

        finally:
            self._window.close()

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

    def estatistica_vida_mana_geral(self, jogadores, npcs):
        column_jogador = self._vida_mana_geral(jogadores, "Jogadores")
        column_npc = self._vida_mana_geral(npcs, "Npcs")

        layout = [
            [sg.Text("STATUS BATALHA")],
            [sg.Column(column_jogador), sg.Column(column_npc)],
            [sg.Button("Voltar", key=MenuCombate.SAIR, size=(13, 2))]
        ]
        self._window = sg.Window("COMBATE", layout)

        try:
            while True:
                event, valores = self._window.read()

                if event == sg.WINDOW_CLOSED or event == MenuCombate.SAIR:
                    return True

        finally:
            self._window.close()

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
            [sg.Button("Voltar", key=MenuCombate.SAIR, size=(13, 2))]
        ]
        self._window = sg.Window("COMBATE", layout)

        try:
            while True:
                event, valores = self._window.read()

                if event == sg.WINDOW_CLOSED or event == MenuCombate.SAIR:
                    return True

        finally:
            self._window.close()

    def desmaiou(self, nome):
        print(f"--------------------------------------------------------------------------")
        print(f"{nome} desmaiou em combate")
