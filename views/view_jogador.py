import time
import PySimpleGUI as sg

from controllers.controller_classe import ControllerClasse
from controllers.controller_poder import ControllerPoder
from exceptions import exceptions
from utils.opcoes_menus import MenuCriacao
from utils.utils import Utils


class ViewJogador:

    def __init__(self, controller_classe: ControllerClasse, controller_poder: ControllerPoder):
        self._window = None
        if not isinstance(controller_classe, ControllerClasse):
            raise TypeError("Controller de classe não é do tipo certo")
        if not isinstance(controller_poder, ControllerPoder):
            raise TypeError("Controller de poderes não é do tipo certo")
        self._controller_classe = controller_classe
        self._controller_poder = controller_poder
        sg.ChangeLookAndFeel('DarkBlue14')

    def criacao_jogador(self, index, nomes_classes, nome_poderes, get_personagem, tamanho_escolha):
        layout = [
            [sg.Text(f"Escolha o nome do {index}º personagem:"),
             sg.InputText(key=MenuCriacao.NOME, size=(26, 2))],
            [sg.Text("Escolha uma classe para o personagem:"),
             sg.Combo(nomes_classes, key=MenuCriacao.SELECIONAR_CLASSE, default_value=nomes_classes[0],
                      enable_events=True, readonly=True)],
            [sg.Text(self._controller_classe.estatisticas_string(nomes_classes[0]),
                     key=MenuCriacao.ESTATISTICAS_CLASSE, background_color=sg.theme_button_color()[1]),
             sg.Text(self._controller_poder.estatisticas(nome_poderes[0]), key=MenuCriacao.ESTATISTICAS_PODER,
                     size=(20, 5), background_color=sg.theme_button_color()[1])],
            [sg.Text(f"Escolha 3 poderes:")],
            [sg.Listbox(values=nome_poderes, size=(26, 5), enable_events=True, key=MenuCriacao.SELECIONAR_PODERES,
                        default_values=nome_poderes[0]),
             sg.Column([[sg.Button("Escolher\n-->", key=MenuCriacao.SELECIONAR_PODER, size=(13, 2))],
                        [sg.Button("<--\nRemover", key=MenuCriacao.REMOVER_PODER, size=(13, 2))]]),
             sg.Listbox(values=[], size=(26, tamanho_escolha), enable_events=True, key=MenuCriacao.ESCOLHIDOS_PODERES),
             ],
            [sg.Button("Voltar", key=MenuCriacao.SAIR, size=(13, 2)),
             sg.Button("Criar Jogador", key=MenuCriacao.CRIAR, size=(13, 2))]
        ]

        self._window = sg.Window("CRIAÇÃO DO GRUPO", layout)

        try:
            while True:
                event, valores = self._window.read()

                if event == sg.WINDOW_CLOSED:
                    raise exceptions.FecharPrograma("Fechar")

                if event == MenuCriacao.SAIR:
                    raise exceptions.VoltarMenu("Voltar")

                if event == MenuCriacao.CRIAR:
                    jogador_dict = self.criar_personagem(valores, get_personagem, tamanho_escolha)
                    if jogador_dict:
                        return jogador_dict

                if event == MenuCriacao.SELECIONAR_CLASSE:
                    classe_selecionada = valores[MenuCriacao.SELECIONAR_CLASSE]
                    self._window.Element(MenuCriacao.ESTATISTICAS_CLASSE).update(
                        self._controller_classe.estatisticas_string(classe_selecionada))

                poderes = self._escolha_poder(event, valores, tamanho_escolha)
                if poderes:
                    return poderes

        finally:
            self._window.close()

    def criar_personagem(self, valores, get_personagem, tamanho_escolha):
        nome = valores[MenuCriacao.NOME]
        classe = valores[MenuCriacao.SELECIONAR_CLASSE]
        poderes = self._window[MenuCriacao.ESCOLHIDOS_PODERES].Values

        # Testa se esse nome já está sendo utilizado
        try:
            get_personagem(nome)
            existe = True
        except exceptions.NaoEncontradoException:
            existe = False

        if not nome:
            sg.popup_error("Escolha um nome para o personagem.")
        elif existe:
            sg.popup_error("Esse nome já está sendo utilizado.")
        elif len(poderes) != tamanho_escolha:
            sg.popup_error(f"Escolha {tamanho_escolha} poderes.")
        else:
            jogador_dict = {
                "nome": nome,
                "classe": classe,
                "poderes": poderes
            }
            return jogador_dict

    def aumentar_nivel(self, nome_jogador: str, nome_classe_antiga: str, estatisticas_classes_nova: dict,
                       nomes_poderes: list[str], nomes_poderes_antigos: list[str]):
        """
        Tela usada para informar que o jogador aumentou de nivel e escolher seus novos poderes
        :param nome_jogador: nome do jogador
        :param nome_classe_antiga: nome da classe antiga do jogador
        :param estatisticas_classes_nova: atributos da classe nova
        :param nomes_poderes: nome dos poderes novos que podem ser selecionados
        :param nomes_poderes_antigos: nome dos poderes que o personagem já possui
        :return: lista com todos os poderes do personagem
        """
        tamanho_escolha = len(nomes_poderes_antigos) + 2

        aviso_aumentou_nivel = f"O {nome_classe_antiga} {nome_jogador}"
        aviso_aumentou_nivel += f" conseguiu experiencia nesse combate e agora é um {estatisticas_classes_nova['nome']}"

        estatisticas_column = [
            [sg.Text(f"Atributos de {nome_jogador}", background_color=sg.theme_button_color()[1])],
            [sg.Text(f"Vida: {estatisticas_classes_nova['vida']}", background_color=sg.theme_button_color()[1])],
            [sg.Text(f"Mana: {estatisticas_classes_nova['mana']}", background_color=sg.theme_button_color()[1])],
            [sg.Text(f"Defesa: {estatisticas_classes_nova['defesa']}", background_color=sg.theme_button_color()[1])],
            [sg.Text(f"Velocidade: {estatisticas_classes_nova['velocidade']}",
                     background_color=sg.theme_button_color()[1])],
        ]

        layout = [
            [sg.Text(aviso_aumentou_nivel)],
            [sg.Column(estatisticas_column, background_color=sg.theme_button_color()[1])],
            [sg.Listbox(values=nomes_poderes, size=(26, 5), enable_events=True, key=MenuCriacao.SELECIONAR_PODERES,
                        default_values=nomes_poderes[0]),
             sg.Text(self._controller_poder.estatisticas(nomes_poderes[0]), key=MenuCriacao.ESTATISTICAS_PODER,
                     size=(20, 5)),
             sg.Listbox(values=nomes_poderes_antigos, size=(26, tamanho_escolha), enable_events=True,
                        key=MenuCriacao.ESCOLHIDOS_PODERES),
             sg.Button("Remover", key=MenuCriacao.REMOVER_PODER, size=(13, 2))
             ],
            [sg.Button("Escolher", key=MenuCriacao.SELECIONAR_PODER, size=(13, 2))],
            [sg.Button("Voltar", key=MenuCriacao.SAIR, size=(13, 2)),
             sg.Button("OK", key=MenuCriacao.CONTINUAR, size=(13, 2))]
        ]
        self._window = sg.Window("LEVEL UP", layout)

        try:
            while True:
                event, valores = self._window.read()

                if event == sg.WINDOW_CLOSED:
                    raise exceptions.FecharPrograma("Fechar")

                if event == MenuCriacao.SAIR:
                    raise exceptions.VoltarMenu("Voltar para o menu")

                poderes = self._escolha_poder(event, valores, tamanho_escolha)
                if poderes:
                    return poderes
        finally:
            self._window.close()

    def _escolha_poder(self, event, valores, tamanho_escolha):
        """
        Essa função realiza a troca entre a lista de escolha e de selecionados
        Tambem mostra as estatisticas do poder selecionado
        :param event: key do evento que ocorrey
        :param valores: valores da tela
        :param tamanho_escolha: quantidade de poderes a serem escolhidos
        :return:
        """
        if event == MenuCriacao.SELECIONAR_PODERES or event == MenuCriacao.ESCOLHIDOS_PODERES:
            poder_selecionado = valores[event][0]

            if poder_selecionado:
                self._window.Element(MenuCriacao.ESTATISTICAS_PODER).update(
                    self._controller_poder.estatisticas(poder_selecionado))

        if event == MenuCriacao.SELECIONAR_PODER:
            poder_selecionado = valores[MenuCriacao.SELECIONAR_PODERES]
            poderes_selecionados = self._window[MenuCriacao.ESCOLHIDOS_PODERES].Values

            if poder_selecionado and len(poderes_selecionados) < tamanho_escolha and len(
                    poder_selecionado) == 1:
                poderes_selecionados.append(poder_selecionado[0])

                poderes_para_escolher = self._window[MenuCriacao.SELECIONAR_PODERES].Values
                poderes_para_escolher.remove(poder_selecionado[0])
                self._window[MenuCriacao.SELECIONAR_PODERES].update(poderes_para_escolher)
                self._window[MenuCriacao.ESCOLHIDOS_PODERES].update(poderes_selecionados)

        if event == MenuCriacao.REMOVER_PODER:
            poder_selecionado = valores[MenuCriacao.ESCOLHIDOS_PODERES]
            if len(poder_selecionado) == 1:
                poderes_selecionados = self._window[MenuCriacao.ESCOLHIDOS_PODERES].Values
                poderes_selecionados.remove(poder_selecionado[0])
                poderes_para_escolher = self._window[MenuCriacao.SELECIONAR_PODERES].Values
                poderes_para_escolher.append(poder_selecionado[0])
                self._window[MenuCriacao.ESCOLHIDOS_PODERES].update(poderes_selecionados)
                self._window[MenuCriacao.SELECIONAR_PODERES].update(poderes_para_escolher)

        if event == MenuCriacao.CONTINUAR:
            poderes = self._window[MenuCriacao.ESCOLHIDOS_PODERES].Values

            if len(poderes) == tamanho_escolha:
                return poderes
            sg.popup_error(f"Escolha {tamanho_escolha} poderes")
