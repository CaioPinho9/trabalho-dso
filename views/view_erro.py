class ViewErro:
    def apenas_inteiros(self):
        print("Utilize apenas números que estão no intervalo")

    def mana_insuficiente(self):
        print("Você não possui mana suficiente para esse poder!")

    def poder_repetido(self, nome_jogador, poder_nome):
        print(f"O personagem {nome_jogador} já possui o poder {poder_nome}")

    def nome_repetido(self, nome_jogador):
        print(f"O personagem {nome_jogador} já possui existe")

    def erro_inexperado_turno(self, nome_jogador):
        print(f"Ocorreu um erro inexperado durante o turno, {nome_jogador} perdeu seu turno")

    def erro_inexperado_menu(self):
        print(f"Ocorreu um erro inexperado, escolha novamente")
