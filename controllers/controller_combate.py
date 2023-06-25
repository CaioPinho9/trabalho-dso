import random

from controllers.controller_classe import ControllerClasse
from controllers.controller_jogador import ControllerJogador
from controllers.controller_npc import ControllerNpc
from controllers.controller_poder import ControllerPoder
from dao.combate_dao import CombateDAO
from exceptions import exceptions
from models.combate import Combate
from models.jogador import Jogador
from models.npc import Npc
from models.personagem import Personagem
from models.poder import Poder
from utils.opcoes_menus import MenuCombate

from views.view_combate import ViewCombate


class ControllerCombate:
    def __init__(self, controller_jogador: ControllerJogador, controller_npc: ControllerNpc,
                 controller_poder: ControllerPoder, controller_classe: ControllerClasse):
        self.__controller_jogador = controller_jogador
        self.__controller_npc = controller_npc
        self.__controller_poder = controller_poder
        self.__controller_classe = controller_classe
        self.__view_combate = ViewCombate(controller_poder)
        self.__combate_atual = None
        self.__combate_dao = CombateDAO()

    def cadastrar(self, npcs: list[Npc]):
        """Cria um novo combate"""
        combate = Combate(self.__combate_dao.get_next_index(), npcs)

        self.__combate_dao.add(combate)

    def get(self, codigo: int):
        """Retorna um combate especifico"""
        return self.__combate_dao.get(codigo)

    def get_all(self):
        """Retorna todos os combates da lista"""
        return self.__combate_dao.get_all()

    def remover(self, codigo: int):
        """Retorna um combate especifico"""
        self.__combate_dao.remove(codigo)

    def remover_all(self):
        self.__combate_dao.clear_file()

    def resetar_combate_atual(self):
        """Restaura a vida dos personagens e volta ao primeiro turno"""
        self.__controller_jogador.restaurar_vida_mana()
        self.__controller_npc.restaurar_vida_mana()
        self.__combate_atual.contador_turno = 1
        self.__combate_atual.iniciado = False

    def iniciar_combate(self, codigo: int):
        """
        Método principal do combate
        Decide a ordem da batalha
        Decide os turnos
        Calcula o dano
        Enquanto um dos grupos do combate ficar com 0 de vida
        Restaura a vida dos personagens
        :param codigo: Combate que será jogado
        :return: True se os jogadores vencerem
        """

        # Combate selecionado
        self.__combate_atual = self.get(codigo)

        # Insere o grupo atual no combate
        self.__combate_atual.jogadores = self.__controller_jogador.get_all()

        # Seleciona os personagens
        jogadores = self.__combate_atual.jogadores
        npcs = self.__combate_atual.npcs

        # Recebe os nomes de todos os jogadores e npcs separadamente
        nomes_jogadores = self.__controller_jogador.nomes(jogadores)
        nomes_npcs = self.__controller_npc.nomes(npcs)

        # Introduz ao jogador quem está participando
        self.__view_combate.iniciar_combate(nomes_jogadores, nomes_npcs)

        # Decide qual a ordem de ação de acordo com um fator aleatório somado com o atributo do personagem
        # Mostra a tela com a ordem
        if not self.__combate_atual.iniciado:
            self.__ordernar_batalha()

            # Proximo da lista de batalha
            proximo_personagem = self.__combate_atual.proximo_da_batalha()
            self.__combate_atual.iniciado = True
        else:
            proximo_personagem = self.__combate_atual.ordem_de_batalha[-1]

        while True:
            try:
                # Método principal de cada turno, telas de escolhas e calculo da combate em geral
                self.__turno(proximo_personagem)

                # Testa se a batalha já acabou
                continuar, vitoria = self.__testar_personagens_vivos()
                if not continuar:
                    break

                # Prepara o próximo turno
                self.__combate_atual.contador_turno += 1
                self.__combate_dao.update(self.__combate_atual)
                proximo_personagem = self.__combate_atual.proximo_da_batalha()

            except exceptions.VoltarMenu as e:
                pass

        # Garante que a vida e a mana estarão cheias no próximo combate
        self.resetar_combate_atual()
        self.__combate_dao.update(self.__combate_atual)

        if vitoria:
            self.__view_combate.vitoria()
        else:
            self.__view_combate.derrota()

        return vitoria

    def __ordernar_batalha(self):
        """
        Cada personagem joga um dado e soma com sua velocidade para decidir quem começa o turno
        Mostra uma tela mostrando os resultados
        """
        # Seleciona os personagens
        personagens = self.__combate_atual.personagens

        # Ordem para ordenar os personagens pelo resultado
        ordem_batalha = {}
        # Armazena os dados que serão utilizados na tela
        jogadas_resultados = []

        # Todos os jogadores fazem um teste pra ver quem é mais veloz
        for personagem in personagens:
            # Dado de 20 lados
            dado = random.randint(1, 20)
            velocidade = personagem.classe.velocidade
            resultado_velocidade = dado + velocidade

            # Salva os resultados de cada personagem
            ordem_batalha[personagem] = resultado_velocidade
            jogadas_resultados.append(
                {
                    "nome": personagem.nome,
                    "dado": dado,
                    "velocidade": velocidade,
                    "resultado": resultado_velocidade,
                    "jogador": isinstance(personagem, Jogador)
                }
            )

        # Ordena pelo resultado da jogada
        ordem_batalha = sorted(ordem_batalha.items(), key=lambda x: x[1], reverse=True)
        ordem_batalha = [x[0] for x in ordem_batalha]

        # Mostra o resultado final
        self.__view_combate.resultado_ordem_de_batalha(
            jogadas_resultados,
            self.__controller_jogador.nomes(ordem_batalha)
        )

        # Armazena o resultado
        self.__combate_atual.ordem_de_batalha = ordem_batalha
        self.__combate_dao.update(self.__combate_atual)

        return True

    def __turno(self, proximo_personagem: Jogador | Npc):
        # Inicia sendo escolhido a ação do jogador
        while True:
            try:
                is_jogador = isinstance(proximo_personagem, Jogador)
                if is_jogador:
                    # Jogador escolhe um dos itens do menu
                    self.__escolher_turno_jogador(proximo_personagem, self.__combate_atual.contador_turno)

                # Personagem escolhe poder e alvos que serão usados nesse turno
                poder, personagens_alvos = self.__escolher_poder_alvos(proximo_personagem)

                is_ataque = poder.ataque

                # Jogadores são alvos se um npc estiver atacando ou um Jogador estiver curando
                # Npcs são alvos se um jogador estiver atacando ou um Npc estiver curando
                if (is_jogador and is_ataque) or (not is_jogador and not is_ataque):
                    nomes_alvos = self.__controller_npc.nomes(personagens_alvos)
                else:
                    nomes_alvos = self.__controller_jogador.nomes(personagens_alvos)

                break
            except exceptions.SairCombate as e:
                raise e
            except exceptions.VoltarMenu as e:
                pass

        # Quando ele escolher um poder o resultado será calculado
        dano_total, resultados = self.__calcular_poder(personagens_alvos, poder)

        # Mostra os resultados desse turno na tela
        self.__view_combate.resultado_turno(
            nome_jogador=proximo_personagem.nome,
            turno=self.__combate_atual.contador_turno,
            is_jogador=is_jogador,
            nomes_alvos=nomes_alvos,
            nome_poder=poder.nome,
            resultados=resultados,
            vida_mana_jogadores=self.__controller_jogador.vida_mana_estatisticas(self.__combate_atual.jogadores),
            vida_mana_npcs=self.__controller_npc.vida_mana_estatisticas(self.__combate_atual.npcs),
        )

        # Armazena os dados de dano ou cura causados pelo jogador nesse turno
        if isinstance(proximo_personagem, Jogador):
            proximo_personagem.causou_dano(dano_total, is_ataque)
        return True

    def __escolher_turno_jogador(self, jogador: Jogador, turno: int):
        """
        Jogadores podem escolher usar um Poder ou ver estatistica de seus personagens
        :param jogador: Jogador que fará a acao
        :param turno: número do turno
        """

        # Jogador escolhe entre usar poder ou receber um relatório
        while True:
            escolha = self.__view_combate.escolher_acao(jogador.nome, turno)

            if escolha == MenuCombate.USAR_PODER:
                # Usar Poder: continua o fluxo principal
                return True

            elif escolha == MenuCombate.STATUS_BATALHA:
                # Status Batalha: mostra a vida e mana dos personagens do combate
                vida_mana_jogadores = self.__controller_jogador.vida_mana_estatisticas(
                    self.__combate_atual.jogadores
                )
                vida_mana_npcs = self.__controller_npc.vida_mana_estatisticas(self.__combate_atual.npcs)
                self.__view_combate.estatistica_vida_mana_geral(vida_mana_jogadores, vida_mana_npcs)
            elif escolha == MenuCombate.ATRIBUTOS:
                # Atributos: Mostra a vida e mana de um personagem além de seus atributos de classe
                vida_mana_jogador = self.__controller_jogador.vida_mana_estatisticas([jogador])[0]
                atributos_classes = self.__controller_classe.estatisticas_dict(jogador.classe.nome)
                self.__view_combate.estatistica_jogador(vida_mana_jogador, atributos_classes)

    def __escolher_poder_alvos(self, proximo_personagem: Jogador | Npc):
        while True:
            # Poder que será utilizado nesse turno
            poder: Poder = self.__escolher_poder(proximo_personagem)
            try:
                # Escolher quem será atingido pelo poder
                if isinstance(proximo_personagem, Jogador):
                    # Jogadores possuem um menu para escolhar
                    personagens_alvos: list[Personagem] = self.__escolher_alvos(proximo_personagem, poder)
                else:
                    # Npcs escolhem aleatóriamente
                    personagens_alvos: list[Personagem] = self.__escolher_alvos_aleatorios(poder)

                # Reduz a mana do jogador
                proximo_personagem.gastar_mana(poder.mana_gasta)

                return poder, personagens_alvos
            except exceptions.VoltarMenu as e:
                pass

    def __escolher_poder(self, personagem: Jogador | Npc):
        """
        Jogadores podem escolher qual poder usar
        :param personagem: Personagem que fará a acao
        :return: poder escolhido
        """
        if isinstance(personagem, Jogador):
            # Personagem escolhe um dos poderes do menu
            # Mostra ao usuario os poderes de seu personagem
            poderes_disponiveis = personagem.poderes_disponiveis
            poderes_disponiveis.sort(key=lambda obj: (-obj.nivel, obj.nome))
            nomes_poderes = self.__controller_poder.nomes(poderes_disponiveis)

            # Jogador escolhe o ataque
            escolha_poder = self.__view_combate.escolher_poder(personagem.nome, self.__combate_atual.contador_turno,
                                                               nomes_poderes,
                                                               personagem.mana_atual)

            # Poder escolhido
            poder = self.__controller_poder.get(escolha_poder)

        else:
            # Npcs escolhem aleatoriamente um poder que possuem mana suficiente
            poder = random.choice(personagem.poderes_disponiveis)

        return poder

    def __escolher_alvos_aleatorios(self, poder: Poder):
        """
        Npc escolhem alvos aleatóriamente
        :param poder: Poder que será utilizado contra o jogador alvo
        :return: Personagem aleatório
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

    def __escolher_alvos(self, proximo_personagem: Jogador | Npc, poder: Poder):
        """
        Se for um ataque o personaem escolher um numero de inimigos de acordo com a quantidade de alvos do poder
        Sendo cura, pode escolher aliados como alvos
        :param poder: Poder utilizado
        :return: Personagens que serão acertados
        """

        # Seleciona se são aliados ou inimigos os alvos
        if poder.ataque:
            personagens_vivos = self.npcs_vivos()
            vida_mana_alvos = self.__controller_npc.vida_mana_estatisticas(personagens_vivos)
        else:
            personagens_vivos = self.jogadores_vivos()
            vida_mana_alvos = self.__controller_jogador.vida_mana_estatisticas(personagens_vivos)

        # Nomes dos personagens que podem ser alvos
        alvos_disponiveis = self.__controller_jogador.nomes(personagens_vivos)

        # Numero maximo que o poder podera escolher
        alvos_maximos = poder.alvos
        if len(personagens_vivos) < alvos_maximos:
            alvos_maximos = len(personagens_vivos)

        # Atributos do poder
        estatisticas_poder = self.__controller_poder.estatisticas([poder])[0]

        # Escolher alvos
        nomes_personagens_alvos = self.__view_combate.escolher_alvos(
            nome_jogador=proximo_personagem.nome,
            turno=self.__combate_atual.contador_turno,
            estatisticas_poder=estatisticas_poder,
            alvos_disponiveis=alvos_disponiveis,
            alvos_maximos=alvos_maximos,
            vida_mana_alvos=vida_mana_alvos,
            is_jogador_alvo=not poder.ataque
        )

        # Encontra os Personagens pelo nome
        personagens_alvos = []
        for nome in nomes_personagens_alvos:
            if poder.ataque:
                personagem = self.__controller_npc.get(nome)
            else:
                personagem = self.__controller_jogador.get(nome)
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

            # Muda a vida do personagem alvo
            personagem.mudar_vida_atual(dano)

            # Salva os valores para mostrar na tela
            resultados.append(
                self.__resultado_turno(
                    poder=poder,
                    dado=dado,
                    valor_final=valor_final,
                    dano=dano,
                    alvo=personagem,
                )
            )

            # Salva as estatisticas do alvo, receber dano ou cura
            if isinstance(personagem, Jogador):
                personagem.recebeu_dano(dano, poder.ataque)

            dano_total += dano

        return dano_total, resultados

    def __testar_personagens_vivos(self):
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
    def __resultado_turno(poder, dado, valor_final, dano, alvo):
        """
        Cria um dicionário com strings de resposta para a tela
        :param poder: Poder utilizado
        :param dado: Valor rolado pelo dado desse alvo
        :param valor_final: Valor do dado somado com o bonus de acerto
        :param dano: Valor de dano ou cura do alvo
        :param alvo: Alvo escolhido
        :return:
        {
        "dado": String com os valores da rolagem do dado, Apenas existe se for um ataque
        "mensagem": String com o resultado se a rolagem foi um sucesso ou falha
        "desmaiado": String que avisa se o alvo desmaiou, Apenas existe se o alvo desmaiar
        }
        """
        resultado = {}
        nome_poder = poder.nome
        ataque = poder.ataque
        acerto = poder.acerto

        nome_alvo = alvo.nome
        defesa_alvo = alvo.classe.defesa
        vida_alvo = alvo.vida_atual

        if ataque:
            ataque_mensagem = f"causar {dano} de dano"
            resultado["dado"] = f"Rolagem [{dado}]+{acerto} = {valor_final}, Defesa: {defesa_alvo}"
        else:
            ataque_mensagem = f"curar {abs(dano)} de vida"

        if valor_final >= defesa_alvo or not ataque:
            resultado['mensagem'] = f"{nome_poder} foi eficaz! Conseguiu {ataque_mensagem} em {nome_alvo}!"
        else:
            resultado['mensagem'] = f"{nome_poder} errou {nome_alvo}!"

        if vida_alvo == 0:
            resultado['desmaiado'] = f"{nome_alvo} desmaiou em combate"

        return resultado
