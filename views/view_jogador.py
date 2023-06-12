import time
import PySimpleGUI as sg

from models.classe import Classe
from models.poder import Poder
from utils.utils import Utils


class ViewJogador:

    def __init__(self):
        self.window = None
        sg.ChangeLookAndFeel('DarkBlue14')

    def _coluna_classe(self, classe: Classe):
        layout = f"Nome: {str(classe.nome)}\n"
        layout += f"Vida: {str(classe.vida)}\n"
        layout += f"Defesa: {str(classe.defesa)}\n"
        layout += f"Mana: {str(classe.mana)}\n"
        layout += f"Velocidade: {str(classe.velocidade)}"
        return layout

    def _coluna_poder(self, poder: Poder):
        layout = f"[{poder.nome} Nvl{poder.nivel}]\n"
        layout += f"{'Dano' if poder.ataque else 'Cura'}: {poder.dano}\n"
        layout += f"Acerto: {poder.acerto}\n"
        layout += f"Mana: {poder.mana_gasta}\n"
        layout += f"Acerta {poder.alvos} {'alvo' if poder.alvos == 1 else 'alvos'}"
        return layout

    def criacao_jogador(self, index, classes, poderes, quantidade):
        classes_nomes = [classe.nome for classe in classes]
        poderes_nome = [poder.nome for poder in poderes]
        layout = [
            [sg.Text(f"Escolha o nome do {index}º personagem:"), sg.InputText(key="-NAME-", size=(30, 1))],
            [sg.Text("Escolha uma classe para o personagem:"),
             sg.Combo(classes_nomes, key="-CLASSE-", default_value=classes_nomes[0], enable_events=True)],
            [sg.Text(self._coluna_classe(classes[0]), key="-CLASSE_ESTATISTICAS-")],
            [sg.Text(f"Escolha {quantidade} poderes:")],
            [sg.Listbox(values=poderes_nome, size=(15, 5), enable_events=True, key="-PODERES-",
                        default_values=poderes_nome[0]),
             sg.Text(self._coluna_poder(poderes[0]), key="-PODER_ESTATISTICAS-", size=(21, 5)),
             sg.Listbox(values=[], size=(15, 3), enable_events=True, key="-PODERES_ESCOLHIDO-"),
             sg.Button("Remover", key="-PODER_REMOVER-")
             ],
            [sg.Button("Escolher", key="-PODER_BOTAO-")],
            [sg.Button("Voltar", key="-RETORNO-"), sg.Button("Criar Jogador", key="-CRIAR-")]
        ]

        self.window = sg.Window("Player Creation", layout)

        try:
            while True:
                event, valores = self.window.read()

                if event == sg.WINDOW_CLOSED or event == "-RETORNO-":
                    break

                if event == "-CRIAR-":
                    jogador_dict = self.criar_personagem(valores, quantidade)
                    if jogador_dict:
                        return jogador_dict

                if event == "-CLASSE-":
                    classe_selecionada = valores["-CLASSE-"]
                    for index_classe, classe in enumerate(classes):
                        if classe.nome == classe_selecionada:
                            index = index_classe
                            break
                    self.window.Element("-CLASSE_ESTATISTICAS-").update(self._coluna_classe(classes[index]))

                if event == "-PODERES-" or event == "-PODERES_ESCOLHIDO-":
                    poder_selecionado = valores[event]
                    for index_poder, poder in enumerate(poderes):
                        if poder.nome == poder_selecionado[0]:
                            index = index_poder
                            break
                    self.window.Element("-PODER_ESTATISTICAS-").update(self._coluna_poder(poderes[index]))

                if event == "-PODER_BOTAO-":
                    poder_selecionado = valores["-PODERES-"]
                    poderes_selecionados = self.window["-PODERES_ESCOLHIDO-"].Values

                    if len(poderes_selecionados) < 3 and len(poder_selecionado) == 1:
                        poderes_selecionados.append(poder_selecionado[0])

                        poderes_para_escolher = self.window["-PODERES-"].Values
                        poderes_para_escolher.remove(poder_selecionado[0])
                        self.window["-PODERES-"].update(poderes_para_escolher)
                        self.window["-PODERES_ESCOLHIDO-"].update(values=poderes_selecionados)

                if event == "-PODER_REMOVER-":
                    poder_selecionado = valores["-PODERES_ESCOLHIDO-"]
                    if len(poder_selecionado) == 1:
                        poderes_selecionados = self.window["-PODERES_ESCOLHIDO-"].Values
                        poderes_selecionados.remove(poder_selecionado[0])
                        poderes_para_escolher = self.window["-PODERES-"].Values
                        poderes_para_escolher.append(poder_selecionado[0])
                        self.window["-PODERES_ESCOLHIDO-"].update(values=poderes_selecionados)
                        self.window["-PODERES-"].update(poderes_para_escolher)

        except Exception as e:
            print(str(e))
            raise e
        finally:
            self.window.close()

    def criar_personagem(self, valores, quantidade):
        nome = valores["-NAME-"]
        classe = valores["-CLASSE-"]
        poderes = self.window["-PODERES_ESCOLHIDO-"].Values

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
            [sg.Button("Voltar", key="-RETORNO-"), sg.Button("OK", key="-OK-")]
        ]
        self.window = sg.Window("Player Created", layout)

        try:
            while True:
                event, valores = self.window.read()

                if event == sg.WINDOW_CLOSED or event == "-RETORNO-":
                    break

                if event == "-OK-":
                    return True

        except Exception as e:
            raise e
        finally:
            self.window.close()

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
