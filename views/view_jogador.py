import time
import PySimpleGUI as sg

from controllers.controller_classe import ControllerClasse
from controllers.controller_poder import ControllerPoder
from exceptions import exceptions
from utils.enumerate import MenuCriacao
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

    def criacao_jogador(self, index, classes_nomes, poderes_nome, quantidade):
        layout = [
            [sg.Text(f"Escolha o nome do {index}º personagem:"), sg.InputText(key=MenuCriacao.NOME, size=(30, 1))],
            [sg.Text("Escolha uma classe para o personagem:"),
             sg.Combo(classes_nomes, key=MenuCriacao.SELECIONAR_CLASSE, default_value=classes_nomes[0],
                      enable_events=True)],
            [sg.Text(self._controller_classe.estatisticas(classes_nomes[0]), key=MenuCriacao.ESTATISTICAS_CLASSE)],
            [sg.Text(f"Escolha {quantidade} poderes:")],
            [sg.Listbox(values=poderes_nome, size=(15, 5), enable_events=True, key=MenuCriacao.SELECIONAR_PODERES,
                        default_values=poderes_nome[0]),
             sg.Text(self._controller_poder.estatisticas(poderes_nome[0]), key=MenuCriacao.ESTATISTICAS_PODER,
                     size=(21, 5)),
             sg.Listbox(values=[], size=(15, 3), enable_events=True, key=MenuCriacao.ESCOLHIDOS_PODERES),
             sg.Button("Remover", key=MenuCriacao.REMOVER_PODER)
             ],
            [sg.Button("Escolher", key=MenuCriacao.ESCOLHER_PODER)],
            [sg.Button("Voltar", key=MenuCriacao.SAIR), sg.Button("Criar Jogador", key=MenuCriacao.CRIAR)]
        ]

        self._window = sg.Window("CRIAÇÃO DO GRUPO", layout)

        try:
            while True:
                event, valores = self._window.read()

                if event == sg.WINDOW_CLOSED or event == MenuCriacao.SAIR:
                    break

                if event == MenuCriacao.CRIAR:
                    jogador_dict = self.criar_personagem(valores, quantidade)
                    if jogador_dict:
                        return jogador_dict

                if event == MenuCriacao.SELECIONAR_CLASSE:
                    classe_selecionada = valores[MenuCriacao.SELECIONAR_CLASSE]
                    for index_classe, classe in enumerate(classes_nomes):
                        if classe == classe_selecionada:
                            index = index_classe
                            break
                    self._window.Element(MenuCriacao.ESTATISTICAS_CLASSE).update(
                        self._controller_classe.estatisticas(classes_nomes[index])
                    )

                if event == MenuCriacao.SELECIONAR_PODERES or event == MenuCriacao.ESCOLHIDOS_PODERES:
                    poder_selecionado = valores[event]
                    for index_poder, poder in enumerate(poderes_nome):
                        if poder == poder_selecionado[0]:
                            index = index_poder
                            break
                    self._window.Element(MenuCriacao.ESTATISTICAS_PODER).update(
                        self._controller_poder.estatisticas(poderes_nome[index])
                    )

                if event == MenuCriacao.ESCOLHER_PODER:
                    poder_selecionado = valores[MenuCriacao.SELECIONAR_PODERES]
                    poderes_selecionados = self._window[MenuCriacao.ESCOLHIDOS_PODERES].Values

                    if len(poderes_selecionados) < 3 and len(poder_selecionado) == 1:
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

        finally:
            self._window.close()

    def criar_personagem(self, valores, quantidade):
        nome = valores[MenuCriacao.NOME]
        classe = valores[MenuCriacao.SELECIONAR_CLASSE]
        poderes = self._window[MenuCriacao.ESCOLHIDOS_PODERES].Values

        if not nome:
            sg.popup_error("Escolha um nome para o personagem.")
        elif len(poderes) != quantidade:
            sg.popup_error(f"Escolha {quantidade} poderes.")
        else:
            jogador_dict = {
                "nome": nome,
                "classe": classe,
                "poderes": poderes
            }
            return jogador_dict

    def aviso_criado(self, jogador_dict):
        layout = [
            [sg.Text(f"{jogador_dict['nome']}, o {Utils.adjetivo(1)}")],
            [sg.Text(f"Classe: {jogador_dict['classe']}")],
            [sg.Listbox(jogador_dict['poderes'], size=(15, 3), disabled=True)],
            [sg.Button("Voltar", key=MenuCriacao.SAIR), sg.Button("OK", key=MenuCriacao.CONTINUAR)]
        ]
        self._window = sg.Window("JOGADOR CRIADO", layout)

        try:
            while True:
                event, valores = self._window.read()

                if event == sg.WINDOW_CLOSED or event == MenuCriacao.SAIR:
                    raise exceptions.VoltarMenu("Voltar para o menu")

                if event == MenuCriacao.CONTINUAR:
                    return True

        finally:
            self._window.close()

    def escolha_nome(self, index):
        print(f"--------------------------------------------------------------------------")
        return input(f"Escolha o nome do {index}º personagem: ")

    def escolha_classe(self, nome, classes):
        print(f"--------------------------------------------------------------------------")
        return input(f"Escolha uma classe para o personagem {nome}: \n{classes}\n")

    def escolha_poderes(self, quantidade):
        return input(f"Escolha o {quantidade}º poder: ")

    def aviso_escolher_poderes(self, nome, quantidade, poderes_estatisticas):
        print(f"--------------------------------------------------------------------------")
        print(f"Você poder escolher até {quantidade} poderes para {nome}. As opções são: ")
        time.sleep(3)
        print(f"{poderes_estatisticas}\n")

    def aviso_aumento_nivel(self, nome, classe, classe_nova):
        print(f"--------------------------------------------------------------------------")
        print(f"O {classe} {nome} conseguiu experiencia nesse combate e agora é um {classe_nova}")
