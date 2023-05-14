import os
import random
import time

from controllers.controller_classe import ControllerClasse
from controllers.controller_jogador import ControllerJogador
from controllers.controller_npc import ControllerNpc
from controllers.controller_personagem import ControllerPersonagem
from controllers.controller_poder import ControllerPoder
from exceptions.exceptions import NaoEncontradoException, ManaInsuficienteException
from models.combate import Combate
from models.jogador import Jogador
from models.npc import Npc
from models.poder import Poder
from utils.utils import Utils
from views.view_combate import ViewCombate
from views.view_erro import ViewErro


class ControllerCombate:
    def __init__(self, view_combate: ViewCombate, view_erro: ViewErro, controller_jogador: ControllerJogador,
                 controller_npc: ControllerNpc, controller_poder: ControllerPoder, controller_classe: ControllerClasse):
        self.__combates = []
        self.__view_combate = view_combate
        self.__view_erro = view_erro
        self.__controller_jogador = controller_jogador
        self.__controller_npc = controller_npc
        self.__controller_poder = controller_poder
        self.__controller_classe = controller_classe
        self.__combate_atual = None
        self.__codigo = 0

    def cadastrar_combate(self, jogadores: list[Jogador], npcs: list[Npc]):
        combate = Combate(self.__codigo, jogadores, npcs)

        self.__codigo += 1

        self.__combates.append(combate)

    def get_combate(self, codigo: int):
        if not isinstance(codigo, int):
            raise TypeError("codigo deve ser um numero inteiro")

        return self.__combates[codigo]

    def iniciar_combate(self, codigo: int):
        try:
            self.__combate_atual = self.get_combate(codigo)
        except Exception:
            raise NaoEncontradoException("Combate não encontrado")

        # Garante que a vida e a mana estarão cheias
        self.__controller_jogador.restaurar_personagens()
        self.__controller_npc.restaurar_personagens()

        jogadores = self.__combate_atual.jogadores
        npcs = self.__combate_atual.npcs

        # Recebe os nomes de todos os jogadores e npcs separadamente
        nomes_jogadores = self.__controller_jogador.personagens_nomes(jogadores)
        nomes_npcs = self.__controller_npc.personagens_nomes(npcs)

        # Introduz ao jogador quem está participando
        self.__view_combate.iniciar_combate(nomes_jogadores, nomes_npcs)

        time.sleep(5)
        os.system("cls")

        # Decide qual a ordem de ação de acordo com um fator aleatório somado com o atributo do personagem
        ordem_de_batalha = self._ordernar_batalha()
        self.__combate_atual.ordem_de_batalha = ordem_de_batalha

        # Recebe os nomes de todos os personagens juntos de acordo com a ordem de batalha
        nomes_personagens = ControllerPersonagem.personagens_nomes(ordem_de_batalha)
        # Mostra para o usuário a ordem
        self.__view_combate.resultado_ordem_de_batalha(nomes_personagens)
        time.sleep(6)

        # Inicia os turnos até que um dos lados fique com 0 de vida
        continuar = True
        vitoria = False
        contador_turnos = 1
        while continuar:
            os.system("cls")
            # Proximo da lista de batalha
            proximo_personagem = self.__combate_atual.proximo_da_batalha()

            # Avisa quem está jogando
            self.__view_combate.iniciar_turno(proximo_personagem.nome, contador_turnos)
            time.sleep(5)

            try:
                # Inicia sendo escolhido a ação do jogador
                poder = self._escolher_acao(proximo_personagem, contador_turnos)

                # Quando ele escolher um poder o resultado será calculado
                self._calcular_poder(proximo_personagem, poder)
            except Exception as e:
                self.__view_erro.erro_inexperado(proximo_personagem.nome)
                print(e)

            # Mostra a vida de todos os personagens
            vida_jogadores = ControllerPersonagem.personagens_vida_mana_estatisticas(jogadores)
            vida_npcs = ControllerPersonagem.personagens_vida_mana_estatisticas(npcs)
            self.__view_combate.estatistica_vida_geral(vida_jogadores, vida_npcs)
            time.sleep(5)

            continuar, vitoria = self._testar_personagens_vivos()
            contador_turnos += 1

        if vitoria:
            self.__view_combate.vitoria()
        else:
            self.__view_combate.derrota()

        return vitoria

    def _ordernar_batalha(self):
        jogadores = self.__combate_atual.jogadores
        npcs = self.__combate_atual.npcs

        personagens = [*jogadores, *npcs]
        ordem_batalha = {}

        self.__view_combate.separacao()

        # Todos os jogadores fazem um teste pra ver quem é mais veloz
        for personagem in personagens:
            velocidade = personagem.classe.velocidade
            resultado_velocidade = ControllerPersonagem.calcular_velocidade(velocidade)
            ordem_batalha[personagem] = resultado_velocidade
            self.__view_combate.resultado_velocidade("JOGADOR" if isinstance(personagem, Jogador) else "NPC",
                                                     personagem.nome, resultado_velocidade - velocidade,
                                                     velocidade, resultado_velocidade)

        # Ordenando pela velocidade
        ordem_batalha = sorted(ordem_batalha.items(), key=lambda x: x[1], reverse=True)
        return [x[0] for x in ordem_batalha]

    def _escolher_acao(self, personagem, index):
        if isinstance(personagem, Jogador):
            # Pedir input enquanto o usuario não enviar uma resposta válida
            while True:
                # Jogador escolhe entre usar poder ou receber um relatório
                escolha = self.__view_combate.escolher_acao()

                if not Utils.check_inteiro_intervalo(escolha, [0, 3]):
                    self.__view_erro.apenas_inteiros()

                if escolha == "0":
                    # Poder[0]
                    poder = self._escolher_poder(personagem)
                    break
                elif escolha == "1":
                    # Status Batalha[1]
                    vida_jogadores = ControllerPersonagem.personagens_vida_mana_estatisticas(
                        self.__combate_atual.jogadores)
                    vida_npcs = ControllerPersonagem.personagens_vida_mana_estatisticas(self.__combate_atual.npcs)
                    self.__view_combate.estatistica_vida_geral(vida_jogadores, vida_npcs)
                elif escolha == "2":
                    # Atributos[2]
                    self.__view_combate.estatistica_classe(
                        self.__controller_classe.classe_estatisticas(personagem.classe))
                elif escolha == "3":
                    # Atributos[2]
                    self.__view_combate.poder_estatistica(
                        self.__controller_poder.poderes_estatisticas(personagem.poderes)
                    )

                # Limpa a tela e restaura o turno
                time.sleep(4)
                os.system("cls")
                self.__view_combate.iniciar_turno(personagem.nome, index)

        else:
            # NPCs escolher aleatoriamente o poder
            while True:
                poder = random.choice(personagem.poderes)
                # Impede que o npc use um poder que não possui mana
                if poder.mana_gasta <= personagem.mana_atual:
                    personagem.gastar_mana(poder.mana_gasta)
                    break

        return poder

    def _escolher_poder(self, personagem):
        poder = None
        # Pedir input enquanto o usuario não enviar uma resposta válida
        while True:
            # Mostra ao usuario os poderes de seu personagem
            poderes_mensagem = self.__controller_poder.poderes_estatisticas(personagem.poderes)

            # Jogador escolhe o ataque
            escolha_poder = self.__view_combate.escolher_poder(personagem.nome, poderes_mensagem, personagem.mana_atual)

            try:
                if Utils.check_inteiro_intervalo(escolha_poder, [0, len(personagem.poderes) - 1]):
                    poder = personagem.poderes[int(escolha_poder)]

                    if not isinstance(poder, Poder):
                        raise TypeError("poder precisa ser um poder")

                    personagem.gastar_mana(poder.mana_gasta)
                    break
                self.__view_erro.apenas_inteiros()
                time.sleep(3)
                os.system("cls")

            except ManaInsuficienteException:
                self.__view_erro.mana_insuficiente()
                time.sleep(3)
                os.system("cls")

        os.system("cls")

        if poder.ataque:
            if poder.alvos == "1":
                self.__view_combate.poder_escolhido_ataque_unico(poder.nome)
            else:
                self.__view_combate.poder_escolhido_ataque_area(poder.nome, str(poder.alvos))
        else:
            self.__view_combate.poder_escolhido_cura_unica(poder.nome)

        return poder

    def _escolher_alvos_aleatorio(self, poder: Poder):
        if poder.ataque:
            personagens_vivos = self.__controller_jogador.personagens_vivos()
        else:
            personagens_vivos = self.__controller_npc.personagens_vivos()

        personagens_alvos = []
        for _ in range(poder.alvos):
            # Selecionando um inimigo aleatório que ainda não foi selecionado
            personagens_disponiveis = list(set(personagens_vivos) - set(personagens_alvos))
            if not personagens_disponiveis:
                break
            personagem_alvo = random.choice(personagens_disponiveis)
            personagens_alvos.append(personagem_alvo)

        return personagens_alvos

    def _escolher_alvos(self, poder: Poder):
        if poder.ataque:
            personagens_vivos = self.__controller_npc.personagens_vivos()
        else:
            personagens_vivos = self.__controller_jogador.personagens_vivos()

        personagens_alvos = []
        for i in range(poder.alvos):
            # Selecionar um inimigo que ainda não foi selecionado
            personagens_disponiveis = [x for x in personagens_vivos if x not in personagens_alvos]
            if not personagens_disponiveis:
                break

            mensagem_alvos = ControllerPersonagem.personagens_vida_estatisticas_com_index(personagens_disponiveis)

            # Numero maximo que o poder podera escolher
            maximo = poder.alvos
            if len(personagens_vivos) < maximo:
                maximo = len(personagens_vivos)

            while True:
                if poder.ataque:
                    if poder.alvos == 1:
                        personagem_alvo = self.__view_combate.escolher_alvo_unico(mensagem_alvos)
                    else:
                        personagem_alvo = self.__view_combate.escolher_alvo_area(mensagem_alvos, i, maximo)
                else:
                    personagem_alvo = self.__view_combate.escolher_alvo_unico(mensagem_alvos)

                if Utils.check_inteiro_intervalo(personagem_alvo, [0, len(personagens_disponiveis) - 1]):
                    break
                self.__view_erro.apenas_inteiros()

            personagens_alvos.append(personagens_disponiveis[int(personagem_alvo)])

        return personagens_alvos

    def _calcular_poder(self, personagem, poder):
        resultado_acerto = ControllerPersonagem.calcular_acerto(poder)

        if isinstance(personagem, Jogador):
            personagens_alvos = self._escolher_alvos(poder)
        else:
            personagens_alvos = self._escolher_alvos_aleatorio(poder)
            nomes_alvos = ControllerPersonagem.personagens_nomes(personagens_alvos)
            self.__view_combate.escolha_npc(personagem.nome, poder.nome, nomes_alvos)

        dado = resultado_acerto - poder.acerto

        for personagem in personagens_alvos:
            dano = poder.dano

            # Cura inverte o dano para aumentar a vida
            if not poder.ataque:
                dano = poder.dano * -1
                ataque = "aumentar"
            else:
                ataque = "diminuir"

            # Cura sempre acerta, ataques precisam passar pela defesa do inimigo
            if resultado_acerto >= personagem.classe.defesa or not poder.ataque:
                self.__view_combate.resultado_poder_sucesso(poder.nome, dado,
                                                            poder.acerto, resultado_acerto, abs(dano),
                                                            ataque, personagem.nome, personagem.classe.defesa)
            else:
                self.__view_combate.resultado_poder_falha(poder.nome, dado, poder.acerto, resultado_acerto,
                                                          personagem.nome, personagem.classe.defesa)
                dano = 0

            time.sleep(2)
            personagem.mudar_vida_atual(dano)

    def _testar_personagens_vivos(self):
        jogadores = self.__combate_atual.jogadores
        npcs = self.__combate_atual.npcs

        # return Continuar, Vitoria,
        if sum(npc.vida_atual for npc in npcs) == 0:
            return False, True

        if sum(jogador.vida_atual for jogador in jogadores) == 0:
            return False, False

        return True, False
