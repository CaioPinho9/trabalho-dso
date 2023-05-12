import random

from controllers.controller_jogador import ControllerJogador
from controllers.controller_npc import ControllerNpc
from controllers.controller_personagem import ControllerPersonagem
from exceptions.exceptions import DuplicadoException, NaoEncontradoException, ManaInsuficienteException
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
        self.__combate_atual = None

    def cadastrar_combate(self, combate: Combate):
        for combate_existente in self.__combates:
            if combate_existente.codigo == combate.codigo:
                raise DuplicadoException("Esse combate já existe")

        self.__combates.append(combate)

    def get_combate(self, codigo: int):
        if not isinstance(codigo, int):
            raise TypeError("codigo deve ser um numero inteiro")

        for combate in self.__combates:
            if combate.codigo == codigo:
                return combate

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

        # Decide qual a ordem de ação de acordo com um fator aleatório somado com o atributo do personagem
        ordem_de_batalha = self._ordernar_batalha()
        self.__combate_atual.ordem_de_batalha = ordem_de_batalha

        # Recebe os nomes de todos os personagens juntos de acordo com a ordem de batalha
        nomes_personagens = ControllerPersonagem.personagens_nomes(ordem_de_batalha)
        # Mostra para o usuário a ordem
        self.__view_combate.resultado_ordem_de_batalha(nomes_personagens)

        # Inicia os turnos até que um dos lados fique com 0 de vida
        continuar = True
        vitoria = False
        contador_turnos = 0
        while continuar:
            proximo_personagem = self.__combate_atual.proximo_da_batalha()

            self.__view_combate.iniciar_turno(proximo_personagem.nome, contador_turnos)

            self._turno(proximo_personagem)

            # Mostra a vida de todos os personagens
            vida_jogadores = ControllerPersonagem.personagens_vida_mana_estatisticas(jogadores)
            vida_npcs = ControllerPersonagem.personagens_vida_mana_estatisticas(npcs)
            self.__view_combate.estatistica_vida_geral(vida_jogadores, vida_npcs)

            continuar, vitoria = self._testar_personagens_vivos()
            contador_turnos += 1

        if vitoria:
            self.__view_combate.vitoria()
        else:
            self.__view_combate.derrota()

    def _ordernar_batalha(self):
        jogadores = self.__combate_atual.jogadores
        npcs = self.__combate_atual.npcs
        ordem_batalha = {}

        for jogador in jogadores:
            velocidade = jogador.classe.velocidade
            resultado_velocidade = ControllerPersonagem.calcular_velocidade(velocidade)
            ordem_batalha[jogador] = resultado_velocidade
            self.__view_combate.resultado_velocidade("JOGADOR", jogador.nome, resultado_velocidade - velocidade,
                                                     velocidade, resultado_velocidade)

        for npc in npcs:
            velocidade = npc.classe.velocidade
            resultado_velocidade = ControllerPersonagem.calcular_velocidade(velocidade)
            ordem_batalha[npc] = resultado_velocidade
            self.__view_combate.resultado_velocidade("NPC", npc.nome, resultado_velocidade - velocidade,
                                                     velocidade, resultado_velocidade)

        # Ordenando pela velocidade
        ordem_batalha = sorted(ordem_batalha.items(), key=lambda x: x[1], reverse=True)
        return [x[0] for x in ordem_batalha]

    def _turno(self, personagem: Personagem):
        # Inicia sendo escolhido a ação do jogador
        poder, item = self._escolher_poder_item(personagem)

        if not item:
            # Caso ele escolha um poder o resultado será calculado
            self._calcular_poder(personagem, poder)
        else:
            # resultado = ControllerPersonagem.calcular_item(poder)
            pass

        # Todo: Show resultado do turno

    def _escolher_poder_item(self, personagem):
        item = None
        poder = None
        if isinstance(personagem, Jogador):
            # Pedir input enquanto o usuario não enviar uma resposta válida

            while True:
                # Jogador escolhe entre usar poder ou item
                escolha_poder_item = self.__view_combate.escolher_poder_ou_item()

                if Utils.check_inteiro_intervalo(escolha_poder_item, [0, 1]):
                    break
                self.__view_combate.apenas_inteiros()

            # Poder[0], Item[1]
            if escolha_poder_item == "0":
                poder = self._escolher_poder(personagem)

            elif escolha_poder_item == 1:
                item = None

        else:
            # NPCs escolher aleatoriamente o poder
            while True:
                poder = random.choice(personagem.poderes)
                # Impede que o npc use um poder que não possui mana
                if poder.mana_gasta <= personagem.mana_atual:
                    personagem.gastar_mana(poder.mana_gasta)
                    break

        return poder, item

    def _escolher_poder(self, personagem):
        # Pedir input enquanto o usuario não enviar uma resposta válida
        while True:
            # Mostra ao usuario os poderes de seu personagem
            poderes_mensagem = self.__controller_jogador.poderes_estatisticas(personagem)

            # Jogador escolhe o ataque
            escolha_poder = self.__view_combate.escolher_poder(personagem.nome, poderes_mensagem, personagem.mana_atual)

            try:
                if Utils.check_inteiro_intervalo(escolha_poder, [0, len(personagem.poderes) - 1]):
                    poder = personagem.poderes[int(escolha_poder)]
                    personagem.gastar_mana(poder.mana_gasta)
                    break
                self.__view_combate.apenas_inteiros()

            except ManaInsuficienteException:
                self.__view_combate.mana_insuficiente()

        if poder.ataque_cura:
            if poder.alvos == "1":
                self.__view_combate.poder_escolhido_ataque_unico(poder.nome)
            else:
                self.__view_combate.poder_escolhido_ataque_area(poder.nome, str(poder.alvos))
        else:
            self.__view_combate.poder_escolhido_cura_unica(poder.nome)

        return poder

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

            mensagem_alvos = ControllerPersonagem.personagens_vida_estatisticas_com_index(personagens_disponiveis)

            # Numero maximo que o poder podera escolher
            maximo = poder.alvos
            if len(personagens_vivos) < maximo:
                maximo = len(personagens_vivos)

            while True:
                if poder.ataque_cura:
                    if poder.alvos == 1:
                        personagem_alvo = self.__view_combate.escolher_alvo_unico(mensagem_alvos)
                    else:
                        personagem_alvo = self.__view_combate.escolher_alvo_area(mensagem_alvos, i, maximo)
                else:
                    personagem_alvo = self.__view_combate.escolher_alvo_unico(mensagem_alvos)

                if Utils.check_inteiro_intervalo(personagem_alvo, [0, len(personagens_vivos)]):
                    break
                self.__view_combate.apenas_inteiros()

            personagens_alvos.append(personagens_vivos[int(personagem_alvo)])

        return personagens_alvos

    def _calcular_poder(self, personagem, poder):
        dano, resultado_acerto = ControllerPersonagem.calcular_poder(poder)

        if isinstance(personagem, Jogador):
            personagens_alvos = self._escolher_alvos(poder)
        else:
            personagens_alvos = self._escolher_alvos_aleatorio(poder)
            nomes_alvos = ControllerPersonagem.personagens_nomes(personagens_alvos)
            self.__view_combate.escolha_npc(personagem.nome, poder.nome, nomes_alvos)

        if not poder.ataque_cura:
            dano *= -1
            ataque_cura = "aumentar"
        else:
            ataque_cura = "diminuir"

        dado = resultado_acerto - poder.acerto

        if resultado_acerto >= 15:
            self.__view_combate.resultado_poder_sucesso(poder.nome, dado,
                                                        poder.acerto, resultado_acerto, abs(dano),
                                                        ataque_cura)
        else:
            self.__view_combate.resultado_poder_falha(poder.nome, dado, poder.acerto, resultado_acerto)

        for personagem in personagens_alvos:
            personagem.mudar_vida_atual(dano)

    def _testar_personagens_vivos(self):
        jogadores = self.__combate_atual.jogadores
        npcs = self.__combate_atual.npcs

        # return Continuar, Vitoria,
        if sum(npc.vida_atual for npc in npcs) == 0:
            return False, False

        if sum(jogador.vida_atual for jogador in jogadores) == 0:
            return False, True

        return True, False
