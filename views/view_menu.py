class ViewMenu:

    def menu_inicial(self, combates_vencidos):
        print(f"--------------------------------------------------------------------------")
        print("Bem vindo ao RPG (Real Programming Game), você será um grande herói ou um grande fracassado?")
        print("Esse é um jogo que você precisará de muita habilidade (e sorte) para vencer os 3 combates")
        print(f"--------------------------------------------------------------------------")
        print("[MENU INICIAL]")
        print("Criar grupo de personagens[0]")
        print("Mostrar grupo de personagens[1]")
        if combates_vencidos >= 0:
            print(f"Combate Inicial[2]")
        if combates_vencidos >= 1:
            print(f"Combate Intermediário[3]")
        if combates_vencidos >= 2:
            print(f"Combate FINAL[4]")
        print(f"Sair do Jogo[{combates_vencidos + 3}]")
        return input()

    def sair(self):
        print(f"--------------------------------------------------------------------------")
        print("Obrigado por Jogar! Trabalho Nota 10")
        print(f"--------------------------------------------------------------------------")

    def grupo(self, grupo):
        print(f"--------------------------------------------------------------------------")
        print(f"O grupo é formado pelo {grupo}")
