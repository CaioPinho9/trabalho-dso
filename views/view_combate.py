import PySimpleGUI as sg

from exceptions import exceptions
from utils.opcoes_menus import MenuCombate
from utils.utils import Utils


class ViewCombate:
    def __init__(self, controller_poder):
        self._controller_poder = controller_poder
        self._window = None

    @staticmethod
    def _mostrar_turno(nome_personagem: str, turno: int, is_jogador: bool, width: int = None):
        """
        Cria um header para a tela mostrando o jogador desse turno e qual turno está
        :param nome_personagem: Nome do personagem
        :param turno: Contador turno
        :param is_jogador: True se for um Jogador, False se for um Npc
        :param width: Optional, Tamanho do header
        :return:
        """
        layout = [
            [
                sg.Multiline(f"\nTURNO {turno}: {'JOGADOR' if is_jogador else 'NPC'}: {nome_personagem}\n",
                             size=(width, 3),
                             background_color=sg.theme_button_color()[1], justification="center", disabled=True,
                             no_scrollbar=True, text_color=sg.theme_button_color()[0])
            ]
        ]

        return layout

    @staticmethod
    def _vida_mana_geral(vida_mana_personagens: list[dict], is_jogador: bool):
        """
        Prepara uma coluna mostrandao a vida e mana de cada personagem da lista
        :param vida_mana_personagens: Lista de dicionários com o estado de cada personagem
        :param is_jogador: True se for um Jogador, se não Npc
        :return:
        """
        tipo = 'Jogador' if is_jogador else 'Npc'
        if len(vida_mana_personagens) > 1:
            tipo += 'es' if is_jogador else 's'

        column = [[sg.Text(f"{tipo}:", background_color=sg.theme_button_color()[1])]]
        for vida_mana_personagem in vida_mana_personagens:
            vida_mana = f"{vida_mana_personagem['nome']}: "
            vida_mana += f"HP[{vida_mana_personagem['vida_atual']}/{vida_mana_personagem['vida_maxima']}] "
            vida_mana += f"Mana:[{vida_mana_personagem['mana_atual']}/{vida_mana_personagem['mana_maxima']}]"
            column.append([sg.Text(vida_mana, background_color=sg.theme_button_color()[1])])

        return column

    def escolher_acao(self, nome_jogador: str, turno: int):
        """
        Jogador escolhe qual menu ele deseja visualizar nesse turno
        :param nome_jogador: Nome do jogador desse turno
        :param turno: Contador de turnos
        :return:
        """
        layout = self._mostrar_turno(nome_jogador, turno, True, width=30)

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
                    raise exceptions.Desistir("Voltar para o menu")

                if event == MenuCombate.USAR_PODER:
                    return event

                if event == MenuCombate.STATUS_BATALHA:
                    return event

                if event == MenuCombate.ATRIBUTOS:
                    return event

        finally:
            self._window.close()

    def iniciar_combate(self, nomes_jogadores: list[str], nomes_npcs: list[str]):
        """
        Tela que mostra quem está na batalha
        :param nomes_jogadores: Lista dos nomes dos jogadores
        :param nomes_npcs: Lista dos nomes dos npcs
        :return:
        """
        layout = [
            [sg.Text("Nesse combate os seguintes personagens se enfrentarão!")],
            [sg.Text("Quem será o vencedor dessa batalha sangrenta!?")],
            [sg.Listbox(nomes_jogadores, size=(15, len(nomes_jogadores)), disabled=True, no_scrollbar=True),
             sg.Text("vs"),
             sg.Listbox(nomes_npcs, size=(15, len(nomes_npcs)), disabled=True, no_scrollbar=True)],
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
                    raise exceptions.Desistir("Voltar para o menu")

                if event == MenuCombate.CONTINUAR:
                    return True

        finally:
            self._window.close()

    @staticmethod
    def _resultado_velocidade(jogadas_resultados: list[dict]):
        """
        Formata o dicionário com as informações de cada jogada em uma string
        :param jogadas_resultados: Lista de dicionários com os valores de cada jogada
        :return: string formatada para mostrar na tela
        """
        resultado_velocidade = ""
        for index, personagem in enumerate(jogadas_resultados):
            resultado_velocidade += f"{'JOGADOR: ' if personagem['jogador'] else 'NPC: '}"
            resultado_velocidade += f"{personagem['nome']}: "
            resultado_velocidade += f"dado[{personagem['dado']}]"
            resultado_velocidade += f"{'+' if personagem['velocidade'] > 0 else ''}"
            resultado_velocidade += f"{personagem['velocidade']} = {personagem['resultado']}"
            if index != len(jogadas_resultados) - 1:
                resultado_velocidade += "\n\n"

        return resultado_velocidade

    def resultado_ordem_de_batalha(self, jogadas_resultados: list[dict], nomes_ordem: list[str]):
        """
        Tela que mostra o resultado do teste de velocidade para ordenar a batalha
        :param jogadas_resultados: Lista de dicionários com os valores de cada jogada
        :param nomes_ordem: Lista com o nome ordenado dos personagens
        """
        layout = [
            [sg.Text(self._resultado_velocidade(jogadas_resultados))],
            [sg.Text("A ordem de batalha será:")],
            [sg.Listbox(nomes_ordem, size=(15, len(nomes_ordem)), disabled=True, no_scrollbar=True)],
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
                    raise exceptions.Desistir("Volte para o menu")

                if event == MenuCombate.CONTINUAR:
                    return True

        finally:
            self._window.close()

    def escolher_poder(self, nome_jogador: str, turno: int, nomes_poderes: list[str], mana_restante: int):
        """
        Tela mostra os poderes que o jogador pode escolher e as estatisticas do poder
        :param nome_jogador: Nome do jogador
        :param turno: Contador turno
        :param nomes_poderes: Lista com os nomes dos poderes
        :param mana_restante: Quanta mana o personagem ainda possui
        :return: Nome do poder escolhido
        """
        layout = self._mostrar_turno(nome_jogador, turno, True, 72)

        layout += [
            [sg.Text(f"O personagem {nome_jogador} tem {mana_restante} de mana sobrando e pode usar esses poderes:")],
            [sg.Listbox(values=nomes_poderes, size=(26, 5), enable_events=True, key=MenuCombate.SELECIONAR_PODER,
                        default_values=nomes_poderes[0]),
             sg.Text(self._controller_poder.estatisticas(nomes_poderes[0]), key=MenuCombate.ESTATISTICAS_PODER,
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
                    raise exceptions.VoltarMenu("Fechar")

                if event == MenuCombate.SELECIONAR_PODER:
                    poder_selecionado = valores[event][0]

                    if poder_selecionado:
                        self._window.Element(MenuCombate.ESTATISTICAS_PODER).update(
                            self._controller_poder.estatisticas(poder_selecionado))

                if event == MenuCombate.CONTINUAR:
                    poder_selecionado = valores[MenuCombate.SELECIONAR_PODER][0]

                    if poder_selecionado:
                        return poder_selecionado
                    sg.popup_error(f"Escolha um poder.")

        finally:
            self._window.close()

    def escolher_alvos(self, nome_jogador: str, turno: int, estatisticas_poder: dict, alvos_disponiveis: list[str],
                       alvos_maximos: int, vida_mana_alvos: list[dict], is_jogador_alvo: bool):
        layout = self._mostrar_turno(nome_jogador, turno, True, 39)

        efeito = "acertar" if estatisticas_poder['ataque'] else "curar"
        efeito += " até" if alvos_maximos > 0 else ""

        layout += [
            [sg.Text(f"O poder {estatisticas_poder['nome']} pode {efeito} {estatisticas_poder['alvos']} alvos")],
            [sg.Listbox(alvos_disponiveis, size=(15, len(alvos_disponiveis)), no_scrollbar=True,
                        key=MenuCombate.SELECIONAR_ALVOS, enable_events=True,
                        select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE),
             sg.Column(self._vida_mana_geral(vida_mana_alvos, is_jogador_alvo), key=MenuCombate.ESTATISTICAS_ALVO,
                       background_color=sg.theme_button_color()[1])],
            [sg.Button("Voltar", key=MenuCombate.SAIR, size=(13, 2)),
             sg.Button("Continuar", key=MenuCombate.CONTINUAR, size=(13, 2))]
        ]

        self._window = sg.Window("COMBATE", layout)

        try:
            while True:
                event, valores = self._window.read()

                if event == sg.WINDOW_CLOSED:
                    raise exceptions.FecharPrograma("Fechar")

                if event == MenuCombate.SAIR:
                    raise exceptions.VoltarMenu("Voltar escolha de ação")

                if event == MenuCombate.CONTINUAR:
                    alvos_selecionados = valores[MenuCombate.SELECIONAR_ALVOS]
                    if len(alvos_selecionados) == alvos_maximos:
                        return alvos_selecionados
                    sg.popup_error(f"Escolha {alvos_maximos} alvos.")

        finally:
            self._window.close()

    def resultado_turno(self, nome_jogador: str, turno: int, is_jogador: bool, nomes_alvos: list[str], nome_poder: str,
                        resultados: list[dict], vida_mana_jogadores: list[dict], vida_mana_npcs: list[dict]):
        """
        Tela que mostra a rolagem dos dados e o estado da batalha apos esse turno
        :param nome_jogador: Nome do jogador
        :param turno: Contador turno
        :param is_jogador: True se é um Jogador, False se for um Npc
        :param nomes_alvos: Lista com o nome dos alvos
        :param nome_poder: Nome do poder escolhido
        :param resultados: Lista de dicionários com strings de resposta
        :param vida_mana_jogadores: Vida e mana dos jogadores
        :param vida_mana_npcs: Vida e mana dos npcs
        """
        layout = self._mostrar_turno(nome_jogador, turno, is_jogador)

        layout += [
            [sg.Text(f"O Poder {nome_poder} será usado em {Utils.list_to_string(nomes_alvos)}")],
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

        column_jogador = self._vida_mana_geral(vida_mana_jogadores, True)
        column_npc = self._vida_mana_geral(vida_mana_npcs, False)
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
                    raise exceptions.Desistir("Volte para o menu")

                if event == MenuCombate.CONTINUAR:
                    return True

        finally:
            self._window.close()

    def estatistica_vida_mana_geral(self, vida_mana_jogadores: list[dict], vida_mana_npcs: list[dict]):
        """
        Tela que mostra o estado atual da batalha
        :param vida_mana_jogadores: Lista de dicionários com o estado de cada jogador
        :param vida_mana_npcs: Lista de dicionários com o estado de cada npc
        """
        column_jogador = self._vida_mana_geral(vida_mana_jogadores, True)
        column_npc = self._vida_mana_geral(vida_mana_npcs, False)

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
        """Tela que avisa que o combate foi uma vitória"""
        layout = [
            [sg.Text("Parabéns! Vocês venceram essa batalha.")],
            [sg.Button("Continuar", key=MenuCombate.SAIR, size=(13, 2))]
        ]

        self.window = sg.Window("VITÓRIA", layout)

        try:
            while True:
                event, valores = self.window.read()

                if event == sg.WINDOW_CLOSED:
                    raise exceptions.FecharPrograma("Fechar")

                if event == MenuCombate.SAIR:
                    return True
        finally:
            self.window.close()

    def derrota(self):
        """
        Tela que mostra que o combate foi uma derrota
        :return:
        """
        layout = [
            [sg.Text("GAME OVER")],
            [sg.Button("Continuar", key=MenuCombate.SAIR, size=(13, 2))]
        ]

        self.window = sg.Window("VITÓRIA", layout)

        try:
            while True:
                event, valores = self.window.read()

                if event == sg.WINDOW_CLOSED:
                    raise exceptions.FecharPrograma("Fechar")

                if event == MenuCombate.SAIR:
                    return True
        finally:
            self.window.close()

    def estatistica_jogador(self, jogador_dict, classe_dict):
        """
        Mostra os atributos de um jogador e seu estado atual
        :param jogador_dict: Dicionário com o nome, vida e mana de um jogador
        :param classe_dict: Atributos de classe do jogador
        """
        layout = [
            [sg.Column([
                [sg.Text(f"Atributos de {jogador_dict['nome']}", background_color=sg.theme_button_color()[1])],
                [sg.Text(f"Vida: {jogador_dict['vida_atual']}/{classe_dict['vida']}",
                         background_color=sg.theme_button_color()[1])],
                [sg.Text(f"Mana: {jogador_dict['mana_atual']}/{classe_dict['mana']}",
                         background_color=sg.theme_button_color()[1])],
                [sg.Text(f"Defesa: {classe_dict['defesa']}", background_color=sg.theme_button_color()[1])],
                [sg.Text(f"Velocidade: {classe_dict['velocidade']}", background_color=sg.theme_button_color()[1])]
            ], background_color=sg.theme_button_color()[1])],
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
