import os
import random
import time

from controllers.controller_classe import ControllerClasse
from controllers.controller_jogador import ControllerJogador
from controllers.controller_npc import ControllerNpc
from controllers.controller_poder import ControllerPoder
from exceptions import exceptions
from models.combate import Combate
from models.jogador import Jogador
from models.npc import Npc
from models.personagem import Personagem
from models.poder import Poder
from utils.opcoes_menus import MenuCombate
from utils.utils import Utils
from views.view_combate import ViewCombate
from views.view_erro import ViewErro


class ControllerCombate:
    def __init__(self, view_erro: ViewErro, controller_jogador: ControllerJogador,
                 controller_npc: ControllerNpc, controller_poder: ControllerPoder, controller_classe: ControllerClasse):
        self.__combates = []
        self.__view_combate = ViewCombate()
        self.__view_erro = view_erro
        self.__controller_jogador = controller_jogador
        self.__controller_npc = controller_npc
        self.__controller_poder = controller_poder
        self.__controller_classe = controller_classe
        self.__combate_atual = None
        self.__codigo = 0

    def cadastrar_combate(self, npcs: list[Npc]):
        """Cria um novo combate"""
        combate = Combate(self.__codigo, npcs)

        self.__codigo += 1

        self.__combates.append(combate)

    def get_combate(self, codigo: int):
        """Retorna um combate especifico"""
        if not isinstance(codigo, int):
            raise TypeError("codigo deve ser um numero inteiro")
        try:
            combate = self.__combates[codigo]
        except Exception:
            raise exceptions.NaoEncontradoException()
        return combate

    def remover_combate(self, codigo: int):
        """Retorna um combate especifico"""
        if not isinstance(codigo, int):
            raise TypeError("codigo deve ser um numero inteiro")
        try:
            self.__combates.pop(codigo)
        except Exception:
            raise exceptions.NaoEncontradoException()

    def iniciar_combate(self, codigo: int):
        """
        Método principal do combate
        Restaura a vida dos personagens
        Decide a ordem da batalha
        Decide os turnos
        Calcula o dano
        Enquanto um dos grupos do combate ficar com 0 de vida
        :param codigo: Combate que será jogado
        :return: True se os jogadores vencerem
        """
        try:
            self.__combate_atual = self.get_combate(codigo)
        except Exception:
            raise exceptions.NaoEncontradoException("Combate não encontrado")

        self.__combate_atual.jogadores = self.__controller_jogador.personagens

        # Garante que a vida e a mana estarão cheias
        self.__controller_jogador.restaurar_vida_mana()
        self.__controller_npc.restaurar_vida_mana()

        jogadores = self.__combate_atual.jogadores
        npcs = self.__combate_atual.npcs

        # Recebe os nomes de todos os jogadores e npcs separadamente
        nomes_jogadores = self.__controller_jogador.nomes(jogadores)
        nomes_npcs = self.__controller_npc.nomes(npcs)

        # Introduz ao jogador quem está participando
        self.__view_combate.iniciar_combate(nomes_jogadores, nomes_npcs)

        # Decide qual a ordem de ação de acordo com um fator aleatório somado com o atributo do personagem
        self._ordernar_batalha()

        # Inicia os turnos até que um dos lados fique com 0 de vida
        continuar = True
        vitoria = False
        contador_turnos = 1
        while continuar:
            # Proximo da lista de batalha
            proximo_personagem = self.__combate_atual.proximo_da_batalha()

            # Avisa quem está jogando

            try:
                # Inicia sendo escolhido a ação do jogador
                poder = self._escolher_turno(proximo_personagem, contador_turnos)

                # Escolhe um ou mais alvos
                if isinstance(proximo_personagem, Jogador):
                    personagens_alvos = self.__escolher_alvos(poder)
                else:
                    personagens_alvos = self.__escolher_alvos_aleatorios(poder)
                    nomes_alvos = self.__controller_jogador.nomes(personagens_alvos)
                    self.__view_combate.escolha_npc(proximo_personagem.nome, poder.nome, nomes_alvos)

                # Quando ele escolher um poder o resultado será calculado
                dano = self.__calcular_poder(personagens_alvos, poder)

                if isinstance(proximo_personagem, Jogador):
                    if dano > 0:
                        proximo_personagem.causou_dano(dano)
                    else:
                        proximo_personagem.causou_cura(abs(dano))

            except exceptions.CombateAcabouException as e:
                raise e
            except Exception as e:
                self.__view_erro.erro_inexperado_turno(proximo_personagem.nome)
                print(e)

            # Mostra a vida de todos os personagens
            vida_jogadores = self.__controller_jogador.vida_mana_estatisticas(jogadores)
            vida_npcs = self.__controller_npc.vida_mana_estatisticas(npcs)
            self.__view_combate.estatistica_vida_mana_geral(vida_jogadores, vida_npcs)
            time.sleep(5)

            continuar, vitoria = self._testar_personagens_vivos()
            contador_turnos += 1

        os.system("cls")
        if vitoria:
            self.__view_combate.vitoria()
        else:
            self.__view_combate.derrota()

        return vitoria

    def _ordernar_batalha(self):
        """
        Cada personagem joga um dado e soma com sua velocidade para decidir quem começa o turno
        :return: Retorna um lista de personagens já na ordem que será jogado
        """
        jogadores = self.__combate_atual.jogadores
        npcs = self.__combate_atual.npcs

        personagens = [*jogadores, *npcs]
        ordem_batalha = {}
        ordem_display = []

        # Todos os jogadores fazem um teste pra ver quem é mais veloz
        for personagem in personagens:
            velocidade = personagem.classe.velocidade

            dado = random.randint(1, 20)

            resultado_velocidade = dado + velocidade

            ordem_batalha[personagem] = resultado_velocidade
            ordem_display.append({"nome": personagem.nome, "dado": dado, "velocidade": velocidade,
                                  "resultado": resultado_velocidade,
                                  "jogador": isinstance(personagem, Jogador)})

        # Mostra para o usuário a ordem
        ordem_batalha = sorted(ordem_batalha.items(), key=lambda x: x[1], reverse=True)
        ordem_batalha = [x[0] for x in ordem_batalha]
        if not self.__view_combate.resultado_ordem_de_batalha(ordem_display,
                                                              self.__controller_jogador.nomes(ordem_batalha)):
            raise exceptions.CombateAcabouException("Volte para o menu")

        self.__combate_atual.ordem_de_batalha = ordem_batalha

        # Ordenando pela velocidade
        return True

    def _escolher_turno(self, personagem: Personagem, index: int):
        """
        É dividido entre a Jogador e Npc
        Jogadores podem escolher usar um Poder ou ver estatistica de seus personagens
        Npcs usam um poder aleatóriamente
        :param personagem: Personagem que fará a acao
        :param index: número do turno
        :return: poder escolhido
        """
        if isinstance(personagem, Jogador):
            # Personagem escolhe um dos itens do menu
            poder = self.__escolher_turno_jogador(personagem, index)

        else:
            # NPCs escolher aleatoriamente o poder
            while True:
                poder = random.choice(personagem.poderes)
                # Impede que o npc use um poder que não possui mana
                if poder.mana_gasta <= personagem.mana_atual and poder.nome != "Soco":
                    personagem.gastar_mana(poder.mana_gasta)
                    break

        return poder

    def __escolher_turno_jogador(self, personagem: Jogador, index: int):
        """
        Jogadores podem escolher usar um Poder ou ver estatistica de seus personagens
        :param personagem: Jogador que fará a acao
        :param index: número do turno
        :return: poder escolhido
        """
        # Pedir input enquanto o usuario não enviar uma resposta válida
        while True:
            # Jogador escolhe entre usar poder ou receber um relatório
            escolha = self.__view_combate.escolher_acao(personagem.nome, index)

            if escolha == MenuCombate.USAR_PODER:
                # Poder[0]
                return self.__escolher_poder(personagem)

            elif escolha == MenuCombate.STATUS_BATALHA:
                # Status Batalha[1]
                vida_mana_jogadores = self.__controller_jogador.vida_mana_estatisticas(
                    self.__combate_atual.jogadores
                )
                vida_mana_npcs = self.__controller_npc.vida_mana_estatisticas(self.__combate_atual.npcs)
                self.__view_combate.estatistica_vida_mana_geral(vida_mana_jogadores, vida_mana_npcs)
            elif escolha == MenuCombate.ATRIBUTOS:
                # Atributos[2]
                vida_mana_jogador = self.__controller_jogador.vida_mana_estatisticas([personagem])[0]
                atributos_classes = self.__controller_classe.classe_estatisticas(personagem.classe)
                self.__view_combate.estatistica_classe(vida_mana_jogador, atributos_classes)
            elif escolha == MenuCombate.LISTAR_PODERES:
                # Poderes[3]
                self.__view_combate.poder_estatistica(
                    self.__controller_poder.poderes_estatisticas(personagem.poderes)
                )

    def __escolher_poder(self, personagem: Jogador):
        """
        Pede para o jogador escolher um poder, até que ele envie uma opção válida
        :param personagem: Jogador que usará o poder
        :return: poder escolhido
        """
        # Pedir input enquanto o usuario não enviar uma resposta válida
        os.system("cls")
        while True:
            # Mostra ao usuario os poderes de seu personagem
            poderes_mensagem = self.__controller_poder.poderes_estatisticas(personagem.poderes)

            # Jogador escolhe o ataque
            escolha_poder = self.__view_combate.escolher_poder(personagem.nome, poderes_mensagem, personagem.mana_atual)

            try:
                Utils.check_inteiro_intervalo(escolha_poder, [0, len(personagem.poderes) - 1])

                poder = personagem.poderes[int(escolha_poder)]

                if not isinstance(poder, Poder):
                    raise TypeError("poder precisa ser um poder")

                personagem.gastar_mana(poder.mana_gasta)
                break

            except exceptions.ManaInsuficienteException:
                self.__view_erro.mana_insuficiente()
                time.sleep(3)
                os.system("cls")
            except TypeError:
                self.__view_erro.apenas_inteiros()
                time.sleep(3)
                os.system("cls")

        os.system("cls")

        # Avisa qual poder foi escolhido e quantos alvos ele pode acertar
        alvos_mensagem = "um alvo" if poder.alvos == 1 else f"até {str(poder.alvos)} alvos"
        ataque_mensagem = "acertar" if poder.ataque else "curar"
        self.__view_combate.poder_escolhido(poder.nome, ataque_mensagem, alvos_mensagem)

        return poder

    def __escolher_alvos_aleatorios(self, poder: Poder):
        """
        Npc escolhem alvos aleatóriamente
        :param poder: Poder que será utilizado contra o jogador alvo
        :return: Jogador aleatório
        """

        # Se for um ataque acerta um jogador, se não cura um npc
        if poder.ataque:
            personagens_vivos = self.jogadores_vivos()
        else:
            personagens_vivos = self.npcs_vivos()

        # Poderes podem ter mais de um alvo
        personagens_alvos = []
        for _ in range(poder.alvos):
            # Selecionando um inimigo aleatório que ainda não foi selecionado
            personagens_disponiveis = [x for x in personagens_vivos if x not in personagens_alvos]

            # Se não tiver mais opções acaba a seleção
            if not personagens_disponiveis:
                break
            personagem_alvo = random.choice(personagens_disponiveis)
            personagens_alvos.append(personagem_alvo)

        return personagens_alvos

    def __escolher_alvos(self, poder: Poder):
        """
        Se for um ataque o jogador escolher um numero de inimigos de acordo com a quantidade de alvos do poder
        Sendo cura, pode escolher aliados como alvos
        :param poder: Poder utilizado
        :return: Personagens que serão acertados
        """

        # Seleciona se são aliados ou inimigos os alvos
        if poder.ataque:
            personagens_vivos = self.npcs_vivos()
        else:
            personagens_vivos = self.jogadores_vivos()

        personagens_alvos = []
        for i in range(poder.alvos):
            # Selecionar um inimigo que ainda não foi selecionado
            personagens_disponiveis = [x for x in personagens_vivos if x not in personagens_alvos]
            if not personagens_disponiveis:
                break

            # Mostra a vida restante dos personagens alvos
            mensagem_alvos = self.__controller_jogador.vida_estatisticas_com_index(personagens_disponiveis)

            # Numero maximo que o poder podera escolher
            maximo = poder.alvos
            if len(personagens_vivos) < maximo:
                maximo = len(personagens_vivos)

            while True:
                try:
                    alvos_selecionados = ""
                    # Ataques em área indicam quantos alvos faltam para selecionar
                    if poder.alvos != 1:
                        alvos_selecionados = f"Alvos selecionados[{i}/{maximo}]\n"

                    personagem_alvo = self.__view_combate.escolher_alvos(mensagem_alvos, alvos_selecionados)

                    Utils.check_inteiro_intervalo(personagem_alvo, [0, len(personagens_disponiveis) - 1])
                    break
                except TypeError:
                    self.__view_erro.apenas_inteiros()
                    time.sleep(3)
                    os.system("cls")

            personagens_alvos.append(personagens_disponiveis[int(personagem_alvo)])

        return personagens_alvos

    def __calcular_poder(self, personagens_alvos, poder):
        """
        Calcula quanto de vida será alterado em cada personagem alvo
        :param personagens_alvos: alvos que serão atingidos
        :param poder: poder que foi usado
        """
        # Calcula o numero rolado no dado
        dado = random.randint(1, 20)

        # Resultado com o bonus do poder
        resultado_acerto = dado + poder.acerto

        for personagem in personagens_alvos:
            dano = poder.dano

            # Cura sempre acerta e inverte o dano para aumentar a vida
            if not poder.ataque:
                dano = poder.dano * -1
                self.__view_combate.resultado_cura(poder.nome, abs(dano), personagem.nome)

            # Ataques precisam passar pela defesa do inimigo
            elif resultado_acerto >= personagem.classe.defesa:
                self.__view_combate.resultado_poder_sucesso(poder.nome, dado,
                                                            poder.acerto, resultado_acerto, dano,
                                                            personagem.nome, personagem.classe.defesa)
            else:
                self.__view_combate.resultado_poder_falha(poder.nome, dado, poder.acerto, resultado_acerto,
                                                          personagem.nome, personagem.classe.defesa)
                dano = 0

            personagem.mudar_vida_atual(dano)

            if isinstance(personagem, Jogador):
                if poder.ataque:
                    personagem.recebeu_dano(dano)
                else:
                    personagem.recebeu_cura(abs(dano))

            # Mostra se um personagem desmaiou
            if personagem.vida_atual == 0:
                self.__view_combate.desmaiou(personagem.nome)

            time.sleep(1)
            return dano

    def _testar_personagens_vivos(self):
        """
        Testa se ainda tem personagens vivos nos dois grupos
        :return: (continuar os turnos, vitoria ou derrota)
        """
        jogadores = self.__combate_atual.jogadores
        npcs = self.__combate_atual.npcs

        # return Continuar, Vitoria,
        if sum(npc.vida_atual for npc in npcs) == 0:
            return False, True

        if sum(jogador.vida_atual for jogador in jogadores) == 0:
            return False, False

        return True, False

    def npcs_vivos(self):
        """
        Npcs que possuem a vida atual acima de 0 ainda estão vivos
        :return: Npcs com vida atual acima de 0
        """
        return [npc for npc in self.__combate_atual.npcs if npc.vida_atual > 0]

    def jogadores_vivos(self):
        """
        Jogadores que possuem a vida atual acima de 0 ainda estão vivos
        :return: Jogadores com vida atual acima de 0
        """
        return [jogador for jogador in self.__combate_atual.jogadores if jogador.vida_atual > 0]
