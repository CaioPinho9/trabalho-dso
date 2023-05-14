class ViewCombate:

    def escolher_acao(self):
        return input("Opções: \nUsar Poder[0]\nStatus Batalha[1]\nAtributos[2]\nLista Poderes[3]\n")

    def escolher_poder(self, nome_personagem, opcoes_poderes, mana):
        print(f"--------------------------------------------------------------------------")
        return input(
            f"O personagem {nome_personagem} tem {mana} de mana sobrando e pode usar esses poderes:\n" +
            opcoes_poderes + "\n")

    def poder_escolhido(self, poder_nome, ataque, alvos):
        print(f"--------------------------------------------------------------------------")
        print(f"O poder {poder_nome} pode {ataque} {alvos}")

    def escolher_alvos(self, opcoes_alvos, area):
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

    def resultado_poder_sucesso(self, poder, dado, acerto, resultado, dano, alvo_nome, alvo_defesa):
        print(f"--------------------------------------------------------------------------")
        print(f"Rolagem [{dado}]+{acerto} = {resultado}, Defesa: {alvo_defesa}")
        print(f"{poder} foi eficaz! Conseguiu causar {dano} de dano em {alvo_nome}!")

    def resultado_poder_falha(self, poder, dado, acerto, resultado, alvo_nome, alvo_defesa):
        print(f"--------------------------------------------------------------------------")
        print(f"Rolagem [{dado}]+{acerto} = {resultado}, Defesa: {alvo_defesa}")
        print(f"{poder} errou {alvo_nome}! ")

    def resultado_cura(self, poder, dano, alvo_nome):
        print(f"--------------------------------------------------------------------------")
        print(f"{poder} foi eficaz! Conseguiu curar {dano} ponto de vida em {alvo_nome}!")

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
        print(f"--------------------------------------------------------------------------")

    def separacao(self):
        print(f"--------------------------------------------------------------------------")

    def estatistica_classe(self, classe):
        print(f"--------------------------------------------------------------------------")
        print(classe)

    def poder_estatistica(self, poderes):
        print(f"--------------------------------------------------------------------------")
        print(poderes)

    def desmaiou(self, nome):
        print(f"--------------------------------------------------------------------------")
        print(f"{nome} desmaiou em combate")
