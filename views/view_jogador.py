class ViewJogador:
    def aviso_iniciar(self):
        print(f"--------------------------------------------------------------------------")
        print("Bem vindo ao RPG (Real Programming Game), você será um grande herói ou um grande fracassado?")
        print("Esse é um jogo que você precisará de muita habilidade (e sorte) para vencer os 5 combates")
        print("Primeiramente você irá criar o seu grupo de fracassados!")
        print(f"--------------------------------------------------------------------------")

    def escolha_nome(self, index):
        print(f"--------------------------------------------------------------------------")
        return input(f"Escolha o nome do {index}º personagem: ")

    def escolha_classe(self, classes):
        return input(f"Escolha uma classe para o personagem: \n{classes}\n")

    def escolha_poderes(self, quantidade):
        return input(f"Escolha o {quantidade}º poder: ")

    def aviso_escolher_poderes(self, nome, poderes_estatisticas):
        print(f"--------------------------------------------------------------------------")
        print(f"Você poder escolher até 3 poderes para {nome}")
        print(f"As opções são: \n{poderes_estatisticas}\n")

    def aviso_criado(self, nome, classe, poderes, xingamento):
        print(f"--------------------------------------------------------------------------")
        print(f"O {classe} {nome} será lembrado como um {xingamento} que possuia os poderes {poderes}")
        print(f"--------------------------------------------------------------------------")
