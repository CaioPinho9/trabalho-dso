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
        self.__controller_jogador = controller_jogador
        self.__controller_npc = controller_npc
        self.__controller_poder = controller_poder
        self.__controller_classe = controller_classe
        self.__combate_atual = None
        self.__codigo = 0
        self.__view_erro = view_erro
        self.__view_combate = ViewCombate(controller_poder)
        self._contador_turno = 0

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
        self._contador_turno = 1
        while continuar:
            # Proximo da lista de batalha
            proximo_personagem = self.__combate_atual.proximo_da_batalha()

            while True:
                try:
                    self._turno(proximo_personagem)
                    break
                except exceptions.CombateAcabouException as e:
                    raise e
                except exceptions.FecharPrograma as e:
                    raise e
                except exceptions.VoltarMenuEscolherTurno as e:
                    pass
                except Exception as e:
                    print(str(e))

            # Mostra a vida de todos os personagens
            # vida_jogadores = self.__controller_jogador.vida_mana_estatisticas(jogadores)
            # vida_npcs = self.__controller_npc.vida_mana_estatisticas(npcs)
            # self.__view_combate.estatistica_vida_mana_geral(vida_jogadores, vida_npcs)

            continuar, vitoria = self._testar_personagens_vivos()
            self._contador_turno += 1

        if vitoria:
            self.__view_combate.vitoria()
        else:
            self.__view_combate.derrota()

        return vitoria

    def _turno(self, proximo_personagem):
        # Inicia sendo escolhido a ação do jogador
        while True:
            try:
                if isinstance(proximo_personagem, Jogador):
                    # Personagem escolhe um dos itens do menu
                    self.__escolher_turno_jogador(proximo_personagem, self._contador_turno)

                while True:
                    try:
                        poder = self._escolher_poder(proximo_personagem)
                        if poder:
                            # Escolhe um ou mais alvos
                            if isinstance(proximo_personagem, Jogador):
                                personagens_alvos = self.__escolher_alvos(proximo_personagem, poder)
                                nomes_alvos = self.__controller_npc.nomes(personagens_alvos)
                            else:
                                personagens_alvos = self.__escolher_alvos_aleatorios(poder)
                                nomes_alvos = self.__controller_jogador.nomes(personagens_alvos)
                            break
                    except exceptions.VoltarMenuEscolherPoder as e:
                        pass
                break
            except exceptions.VoltarMenuEscolherTurno as e:
                pass
            except exceptions.CombateAcabouException as e:
                raise e
            except exceptions.FecharPrograma as e:
                raise e

        # Quando ele escolher um poder o resultado será calculado
        dano, resultados = self.__calcular_poder(personagens_alvos, poder)

        self.__view_combate.resultado_turno(
            nome=proximo_personagem.nome,
            turno=self._contador_turno,
            tipo=isinstance(proximo_personagem, Jogador),
            nomes_alvos=nomes_alvos,
            poder=poder.nome,
            resultados=resultados,
            jogadores=self.__controller_jogador.vida_mana_estatisticas(self.__combate_atual.jogadores),
            npcs=self.__controller_npc.vida_mana_estatisticas(self.__combate_atual.npcs),
        )

        if isinstance(proximo_personagem, Jogador):
            if dano > 0:
                proximo_personagem.causou_dano(dano)
            else:
                proximo_personagem.causou_cura(abs(dano))
        return True

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
        self.__view_combate.resultado_ordem_de_batalha(ordem_display, self.__controller_jogador.nomes(ordem_batalha))

        self.__combate_atual.ordem_de_batalha = ordem_batalha

        # Ordenando pela velocidade
        return True

    def _escolher_poder(self, personagem: Personagem):
        """
        É dividido entre a Jogador e Npc
        Jogadores podem escolher escolher qual poder usar
        :param personagem: Personagem que fará a acao
        :return: poder escolhido
        """
        if isinstance(personagem, Jogador):
            # Personagem escolhe um dos itens do menu
            poder = self.__escolher_poder(personagem, self._contador_turno)

        else:
            # NPCs escolher aleatoriamente o poder
            while True:
                poder = random.choice(personagem.poderes)
                # Impede que o npc use um poder que não possui mana
                if poder.mana_gasta <= personagem.mana_atual and poder.nome != "Soco":
                    personagem.gastar_mana(poder.mana_gasta)
                    break

        return poder

    def __escolher_turno_jogador(self, personagem: Jogador, turno: int):
        """
        Jogadores podem escolher usar um Poder ou ver estatistica de seus personagens
        :param personagem: Jogador que fará a acao
        :param turno: número do turno
        :return: poder escolhido
        """
        # Jogador escolhe entre usar poder ou receber um relatório
        while True:
            escolha = self.__view_combate.escolher_acao(personagem.nome, turno)

            if escolha == MenuCombate.USAR_PODER:
                # Poder[0]
                return True

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
                atributos_classes = self.__controller_classe.estatisticas_dict(personagem.classe)
                self.__view_combate.estatistica_classe(vida_mana_jogador, atributos_classes)

    def __escolher_poder(self, personagem: Jogador, turno: int):
        """
        Pede para o jogador escolher um poder, até que ele envie uma opção válida
        :param personagem: Jogador que usará o poder
        :param turno: número do turno atual
        :return: poder escolhido
        """
        # Mostra ao usuario os poderes de seu personagem
        poderes_nome = self.__controller_poder.nomes(personagem.poderes_disponiveis)

        # Jogador escolhe o ataque
        escolha_poder = self.__view_combate.escolher_poder(personagem.nome, turno, poderes_nome, personagem.mana_atual)

        if not escolha_poder:
            return

        poder = self.__controller_poder.get_poder(escolha_poder)

        personagem.gastar_mana(poder.mana_gasta)

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

    def __escolher_alvos(self, proximo_personagem, poder: Poder):
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

        # Nomes dos personagens que podem ser alvos
        alvos_disponiveis = self.__controller_jogador.nomes(personagens_vivos)

        # Numero maximo que o poder podera escolher
        alvos_maximos = poder.alvos
        if len(personagens_vivos) < alvos_maximos:
            alvos_maximos = len(personagens_vivos)

        poder_dict = self.__controller_poder.estatisticas_dict([poder])[0]

        personagens_alvos_nomes = self.__view_combate.escolher_alvos(proximo_personagem.nome, self._contador_turno,
                                                                     poder_dict, alvos_disponiveis, alvos_maximos,
                                                                     not poder.ataque)

        personagens_alvos = []
        for nome in personagens_alvos_nomes:
            if poder.ataque:
                personagem = self.__controller_npc.get_com_nome(nome)
            else:
                personagem = self.__controller_jogador.get_com_nome(nome)
            personagens_alvos.append(personagem)

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
        valor_final = dado + poder.acerto
        dano_total = 0
        resultados = []
        for personagem in personagens_alvos:
            dano = poder.dano

            # Cura sempre acerta e inverte o dano para aumentar a vida
            if not poder.ataque:
                dano = poder.dano * -1

            # Ataques precisam passar pela defesa do inimigo
            elif valor_final < personagem.classe.defesa:
                dano = 0

            personagem.mudar_vida_atual(dano)

            resultados.append(
                self._resultado_turno(
                    poder=poder.nome,
                    ataque=poder.ataque,
                    acerto=poder.acerto,
                    dado=dado,
                    valor_final=valor_final,
                    dano=dano,
                    alvo_nome=personagem.nome,
                    alvo_defesa=personagem.classe.defesa,
                    alvo_vida=personagem.vida_atual,
                )
            )

            if isinstance(personagem, Jogador):
                if poder.ataque:
                    personagem.recebeu_dano(dano)
                else:
                    personagem.recebeu_cura(abs(dano))

            dano_total += dano

        return dano_total, resultados

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

    @staticmethod
    def _resultado_turno(poder, ataque, acerto, dado, valor_final, dano, alvo_nome, alvo_defesa, alvo_vida):
        resultado = {}

        if ataque:
            ataque_mensagem = f"causar {dano} de dano"
            resultado["dado"] = f"Rolagem [{dado}]+{acerto} = {valor_final}, Defesa: {alvo_defesa}"
        else:
            ataque_mensagem = f"curar {abs(dano)} de vida"

        if valor_final >= alvo_defesa or not ataque:
            resultado['mensagem'] = f"{poder} foi eficaz! Conseguiu {ataque_mensagem} em {alvo_nome}!"
        else:
            resultado['mensagem'] = f"{poder} errou {alvo_nome}!"

        if alvo_vida == 0:
            resultado['desmaiado'] = f"{alvo_nome} desmaiou em combate"

        return resultado
