class ViewCombate:

    def escolher_acao(self):
        return input("Opções: \nUsar Poder[0]\nStatus Batalha[1]\nAtributos[2]\nLista Poderes[3]\n")

    def escolher_poder(self, nome_personagem, opcoes_poderes, mana):
        print(f"--------------------------------------------------------------------------")
        return input(
            f"O personagem {nome_personagem} tem {mana} de mana sobrando e pode usar esses poderes:\n" +
            opcoes_poderes + "\n")

    def poder_escolhido_ataque_area(self, poder_nome, maximo):
        print(f"--------------------------------------------------------------------------")
        print(f"O poder {poder_nome} pode acertar até {maximo} alvos")

    def poder_escolhido_ataque_unico(self, poder_nome):
        print(f"--------------------------------------------------------------------------")
        print(f"O poder {poder_nome} pode acertar um alvo")

    def poder_escolhido_cura_unica(self, poder_nome):
        print(f"--------------------------------------------------------------------------")
        print(f"O poder {poder_nome} pode curar um aliado")

    def escolher_alvo_area(self, opcoes_alvos, escolhidos, maximo):
        return input(f"Selecione um alvo:\n{opcoes_alvos}\nAlvos selecionados[{escolhidos}/{maximo}]\n")

    def escolher_alvo_unico(self, opcoes_alvos):
        return input(f"Selecione um alvo:\n{opcoes_alvos}\n")

    def iniciar_combate(self, jogadores, npcs):
        print(f"--------------------------------------------------------------------------")
        print(f"Nesse combate os personagens {jogadores} irão enfrentar os inimigos {npcs}")
        print(f"--------------------------------------------------------------------------")
        print(f"Vamos decidir quem irá começar a batalha!")

    def iniciar_turno(self, personagem, index):
        print(f"--------------------------------------------------------------------------")
        print(f"TURNO {index}: {personagem}")
        print(f"--------------------------------------------------------------------------")

    def resultado_velocidade(self, tipo_personagem, nome, dado, velocidade, resultado):
        print(f"{tipo_personagem} {nome}: [{dado}]+{velocidade} = {resultado}")

    def resultado_ordem_de_batalha(self, ordem):
        print(f"--------------------------------------------------------------------------")
        print(f"A ordem de batalha será {ordem}")

    def resultado_poder_sucesso(self, poder, dado, acerto, resultado, dano, ataque, alvo_nome, alvo_defesa):
        print(f"--------------------------------------------------------------------------")
        print(f"Rolagem [{dado}]+{acerto} = {resultado}, Defesa: {alvo_defesa}")
        print(f"{poder} foi eficaz! Conseguiu {ataque} {dano} ponto de vida em {alvo_nome}!")

    def resultado_poder_falha(self, poder, dado, acerto, resultado, alvo_nome, alvo_defesa):
        print(f"--------------------------------------------------------------------------")
        print(f"Rolagem [{dado}]+{acerto} = {resultado}, Defesa: {alvo_defesa}")
        print(f"{poder} errou {alvo_nome}! ")

    def escolha_npc(self, nome, poder, alvos):
        print(f"NPC {nome} irá usar {poder} em {alvos}")

    def estatistica_vida_geral(self, jogadores, npcs):
        print(f"--------------------------------------------------------------------------")
        print(f"[STATUS BATALHA]")
        print(jogadores)
        print(f"----------------------------")
        print(npcs)

    def vitoria(self):
        print(f"--------------------------------------------------------------------------")
        print("Parabéns! Vocês venceram essa batalha")

    def derrota(self):
        print(f"--------------------------------------------------------------------------")
        print("GAME OVER.")

    def separacao(self):
        print(f"--------------------------------------------------------------------------")

    def estatistica_classe(self, classe):
        print(f"--------------------------------------------------------------------------")
        print(classe)

    def poder_estatistica(self, poderes):
        print(f"--------------------------------------------------------------------------")
        print(poderes)
