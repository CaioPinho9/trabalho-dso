import random

from controllers.controller_jogador import ControllerJogador
from controllers.controller_npc import ControllerNpc
from controllers.controller_personagem import ControllerPersonagem
from exceptions.exceptions import DuplicadoException, NaoEncontradoException
from models.combate import Combate
from models.jogador import Jogador
from models.personagem import Personagem
from models.poder import Poder
from utils.utils import Utils
from views.view_combate import ViewCombate


class ControllerCombate:

    def __init__(self, view_combate: ViewCombate, controller_jogador: ControllerJogador, controller_npc: ControllerNpc):
        self.__combates = []
        self.__view_combate = view_combate
        self.__controller_jogador = controller_jogador
        self.__controller_npc = controller_npc
        self.__combate_atual: Combate = None

    def cadastrar_combate(self, combate: Combate):
        for escolha_poder, combate_existente in enumerate(self.__combates):
            if combate_existente.codigo == combate.codigo:
                raise DuplicadoException("Esse combate já existe")

        self.__combates.append(combate)

    def iniciar_combate(self, codigo: int):
        for escolha_poder, combate_existente in enumerate(self.__combates):
            if combate_existente.codigo == codigo:
                self.__combate_atual = combate_existente

        if not self.__combate_atual:
            raise NaoEncontradoException("Combate não encontrado")

        self.__combate_atual.ordem_de_batalha = self._ordernar_batalha()
        #TODO show ordem

        continuar = True
        while continuar:
            proximo_personagem = self.__combate_atual.proximo_da_batalha()

            self._turno(proximo_personagem)

            continuar, vitoria = self._testar_personagens_vivos()

    def _escolher_alvos_aleatorio(self, poder: Poder):
        if poder.ataque_cura:
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
        if poder.ataque_cura:
            personagens_vivos = self.__controller_npc.personagens_vivos()
        else:
            personagens_vivos = self.__controller_jogador.personagens_vivos()

        personagens_alvos = []
        for i in range(poder.alvos):
            # Selecionando um inimigo aleatório que ainda não foi selecionado
            personagens_disponiveis = list(set(personagens_vivos) - set(personagens_alvos))
            if not personagens_disponiveis:
                break
            opcoes_alvos = [personagem.nome + "[" + str(index) + "]: " +
                            str(personagem.vida_atual) + "/" + str(personagem.classe.vida) for
                            index, personagem in enumerate(personagens_disponiveis)]

            mensagem_alvos = "\n-------------------".join(opcoes_alvos)

            while True:
                if poder.ataque_cura:
                    if poder.alvos == 1:
                        personagem_alvo = self.__view_combate.escolher_alvo_unico(mensagem_alvos)
                    else:
                        personagem_alvo = self.__view_combate.escolher_alvo_area(i + 1, poder.alvos, mensagem_alvos)
                else:
                    personagem_alvo = self.__view_combate.escolher_alvo_unico(mensagem_alvos)
                parar = Utils.check_inteiro_intervalo(personagem_alvo, [0,len(personagens_vivos)])
                if parar:
                    break
                self.__view_combate.escolha_inteiro()

            personagens_alvos.append(personagens_vivos[int(personagem_alvo)])

        return personagens_alvos

    def _turno(self, personagem: Personagem):
        item = None
        poder = None

        if isinstance(personagem, Jogador):
            # Pedir input enquanto o usuario não enviar uma resposta válida

            while True:
                # Jogador escolhe entre usar poder ou item
                escolha_poder_item = self.__view_combate.escolher_poder_ou_item()

                parar = Utils.check_inteiro_intervalo(escolha_poder_item, [0, 1])
                if parar:
                    break
                self.__view_combate.escolha_inteiro()

            # Poder[0], Item[1]
            if escolha_poder_item == "0":
                # Pedir input enquanto o usuario não enviar uma resposta válida
                while True:
                    opcoes_poderes = self.__controller_jogador.poderes_estatisticas(personagem)

                    poderes_mensagem = "\n-------------------".join(opcoes_poderes)

                    escolha_poder = self.__view_combate.escolher_poder(personagem.nome, poderes_mensagem)

                    parar = Utils.check_inteiro_intervalo(escolha_poder, [0, len(opcoes_poderes) - 1])
                    if parar:
                        break
                    self.__view_combate.escolha_inteiro()

                poder = personagem.poderes[int(escolha_poder)]

                if poder.ataque_cura:
                    if poder.alvos == "1":
                        self.__view_combate.poder_escolhido_ataque_unico(poder.nome)
                    else:
                        self.__view_combate.poder_escolhido_ataque_area(poder.nome, str(poder.alvos))
                else:
                    self.__view_combate.poder_escolhido_cura_unica(poder.nome)

            elif escolha_poder_item == 1:
                item = None

        else:
            poder = random.choice(personagem.poderes)

        if not item:
            dano, resultado_acerto = ControllerPersonagem.calcular_poder(poder)

            if isinstance(personagem, Jogador):
                personagens_alvos = self._escolher_alvos(poder)
            else:
                personagens_alvos = self._escolher_alvos_aleatorio(poder)

            if not poder.ataque_cura:
                dano *= -1

            for personagem in personagens_alvos:
                personagem.mudar_vida_atual(dano)
        else:
            # resultado = ControllerPersonagem.calcular_item(poder)
            pass

        # Todo: Show resultado do turno

    def _ordernar_batalha(self):
        jogadores = self.__combate_atual.jogadores
        npcs = self.__combate_atual.npcs
        ordem_batalha = {}

        for jogador in jogadores:
            resultado_velocidade = ControllerPersonagem.calcular_velocidade(jogador.classe.velocidade)
            ordem_batalha[jogador] = resultado_velocidade

        for npc in npcs:
            resultado_velocidade = ControllerPersonagem.calcular_velocidade(npc.classe.velocidade)
            ordem_batalha[npc] = resultado_velocidade

        # Ordenando pela velocidade
        ordem_batalha = sorted(ordem_batalha.items(), key=lambda x: x[1])
        return [x[0] for x in ordem_batalha]

    def _testar_personagens_vivos(self):
        jogadores = self.__combate_atual.jogadores
        npcs = self.__combate_atual.npcs

        # return Continuar, Vitoria,
        if sum(npc.vida_atual for npc in npcs) == 0:
            return False, False

        if sum(jogador.vida_atual for jogador in jogadores) == 0:
            return False, True

        return True, False
