import PySimpleGUI as sg

from exceptions import exceptions
from utils.opcoes_menus import MenuCombate
from utils.utils import Utils


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

    def _mostrar_turno(self, nome, turno, jogador, width=None):
        layout = [
            [
                sg.Multiline(f"\nTURNO {turno}: {'JOGADOR' if jogador else 'NPC'}: {nome}\n", size=(width, 3),
                             background_color=sg.theme_button_color()[1], justification="center", disabled=True,
                             no_scrollbar=True, text_color=sg.theme_button_color()[0])
            ]
        ]

        return layout

    def _mostrar_vida_mana(self, personagem):
        vida_mana = f"{personagem['nome']}: "
        vida_mana += f"HP[{personagem['vida_atual']}/{personagem['vida_maxima']}] "
        vida_mana += f"Mana:[{personagem['mana_atual']}/{personagem['mana_maxima']}]"
        return vida_mana

    def _vida_mana_geral(self, personagens, tipo):
        column = [[sg.Text(f"{tipo}:", background_color=sg.theme_button_color()[1])]]
        for personagem in personagens:
            column.append([sg.Text(self._mostrar_vida_mana(personagem), background_color=sg.theme_button_color()[1])])

        return column

    def escolher_acao(self, nome, turno):
        layout = self._mostrar_turno(nome, turno, True, width=30)

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

                if event == sg.WINDOW_CLOSED:
                    raise exceptions.FecharPrograma("Fechar")

                if event == MenuCombate.SAIR:
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
        layout = self._mostrar_turno(nome_personagem, turno, True, 72)

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
                    raise exceptions.FecharPrograma("Fechar")

                if event == MenuCombate.SAIR:
                    raise exceptions.VoltarMenuEscolherTurno("Fechar")

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

    def escolher_alvos(self, nome_personagem, turno, poder_dict, alvos_disponiveis, alvos_maximos, jogador):
        layout = self._mostrar_turno(nome_personagem, turno, True, 39)

        efeito = "acertar" if poder_dict['ataque'] else "curar"
        efeito += " até" if alvos_maximos > 0 else ""

        layout += [
            [sg.Text(f"O poder {poder_dict['nome']} pode {efeito} {poder_dict['alvos']} alvos")],
            [sg.Listbox(alvos_disponiveis, size=(15, len(alvos_disponiveis)), no_scrollbar=True,
                        key=MenuCombate.SELECIONAR_ALVOS, enable_events=True,
                        select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE)],
            [sg.Button("Voltar", key=MenuCombate.SAIR, size=(13, 2)),
             sg.Button("Continuar", key=MenuCombate.CONTINUAR, size=(13, 2))]
        ]

        # TODO: SHOW TARGETS HEALTH
        self._window = sg.Window("COMBATE", layout)

        try:
            while True:
                event, valores = self._window.read()

                if event == sg.WINDOW_CLOSED:
                    raise exceptions.FecharPrograma("Fechar")

                if event == MenuCombate.SAIR:
                    raise exceptions.VoltarMenuEscolherPoder("Voltar escolha de ação")

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

                if event == sg.WINDOW_CLOSED:
                    exceptions.FecharPrograma("Fechar")

                if event == MenuCombate.SAIR:
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

                if event == sg.WINDOW_CLOSED:
                    raise exceptions.FecharPrograma("Fechar")

                if event == MenuCombate.SAIR:
                    raise exceptions.CombateAcabouException("Volte para o menu")

                if event == MenuCombate.CONTINUAR:
                    return True

        finally:
            self._window.close()

    def resultado_turno(self, nome, turno, tipo, nomes_alvos, poder, resultados, jogadores, npcs):
        layout = self._mostrar_turno(nome, turno, tipo)

        layout += [
            [sg.Text(f"O Poder {poder} será usado em {Utils.list_to_string(nomes_alvos)}")],
        ]

        for index, resultado in enumerate(resultados):
            column = [[sg.Text(f"Alvo {index + 1}: {nomes_alvos[index]}", background_color=sg.theme_button_color()[1])]]
            row = []
            if resultado.get('dado'):
                row.append(
                    sg.Text(f"{resultado['dado']}", background_color=sg.theme_button_color()[1], size=(25, 1))
                )

            row.append(
                sg.Text(f"{resultado['mensagem']}", background_color=sg.theme_button_color()[1])
            )

            column.append(row)

            if resultado.get('desmaiado'):
                column.append(
                    [sg.Text(f"{resultado['desmaiado']}")]
                )
            layout += [[sg.Column(column, background_color=sg.theme_button_color()[1])]]

        column_jogador = self._vida_mana_geral(jogadores, "Jogadores")
        column_npc = self._vida_mana_geral(npcs, "Npcs")
        layout += [[sg.Column(column_jogador, background_color=sg.theme_button_color()[1]),
                    sg.Column(column_npc, background_color=sg.theme_button_color()[1])],
                   [sg.Button("Desistir", key=MenuCombate.SAIR, size=(13, 2)),
                    sg.Button("Continuar", key=MenuCombate.CONTINUAR, size=(13, 2))]
                   ]

        self._window = sg.Window("COMBATE", layout)

        try:
            while True:
                event, valores = self._window.read()

                if event == sg.WINDOW_CLOSED:
                    raise exceptions.FecharPrograma("Fechar")

                if event == MenuCombate.SAIR:
                    raise exceptions.CombateAcabouException("Volte para o menu")

                if event == MenuCombate.CONTINUAR:
                    return True

        finally:
            self._window.close()

    def estatistica_vida_mana_geral(self, jogadores, npcs):
        column_jogador = self._vida_mana_geral(jogadores, "Jogadores")
        column_npc = self._vida_mana_geral(npcs, "Npcs")

        layout = [
            [sg.Text("STATUS BATALHA")],
            [sg.Column(column_jogador, background_color=sg.theme_button_color()[1]),
             sg.Column(column_npc, background_color=sg.theme_button_color()[1])],
            [sg.Button("Voltar", key=MenuCombate.SAIR, size=(13, 2))]
        ]
        self._window = sg.Window("COMBATE", layout)

        try:
            while True:
                event, valores = self._window.read()

                if event == sg.WINDOW_CLOSED:
                    raise exceptions.FecharPrograma("Fechar")

                if event == MenuCombate.SAIR:
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

                if event == sg.WINDOW_CLOSED:
                    raise exceptions.FecharPrograma("Fechar")

                if event == MenuCombate.SAIR:
                    return True

        finally:
            self._window.close()

    def desmaiou(self, nome):
        print(f"--------------------------------------------------------------------------")
        print(f"{nome} desmaiou em combate")
