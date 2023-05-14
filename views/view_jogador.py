import time


class ViewJogador:
    def escolha_nome(self, index):
        print(f"--------------------------------------------------------------------------")
        return input(f"Escolha o nome do {index}º personagem: ")

    def escolha_classe(self, classes):
        return input(f"Escolha uma classe para o personagem: \n{classes}\n")

    def escolha_poderes(self, quantidade):
        return input(f"Escolha o {quantidade}º poder: ")

    def aviso_escolher_poderes(self, nome, quantidade, poderes_estatisticas):
        print(f"--------------------------------------------------------------------------")
        print(f"Você poder escolher até {str(quantidade)} poderes para {nome}. As opções são: ")
        time.sleep(3)
        print(f"{poderes_estatisticas}\n")

    def aviso_criado(self, nome, classe, poderes, adjetivo):
        print(f"--------------------------------------------------------------------------")
        print(f"O {classe} {nome} será lembrado como um {adjetivo} que possuia os poderes:\n{poderes}")
        print(f"--------------------------------------------------------------------------")

    def aviso_aumento_nivel(self, nome, classe, classe_nova):
        print(f"--------------------------------------------------------------------------")
        print(f"O {classe} {nome} conseguiu experiencia nesse combate e agora é um {classe_nova}")


