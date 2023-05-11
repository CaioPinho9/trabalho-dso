class ViewCombate:
    def escolher_poder_ou_item(self):
        return input("Escolha entre usar um poder[0] ou um item[1]:")

    def escolha_inteiro(self):
        print("Utilize apenas números que estão no intervalo")

    def escolher_poder(self, nome_personagem, opcoes_poderes):
        return input("O personagem " + nome_personagem + " pode usar esses poderes:\n" + opcoes_poderes)

    def poder_escolhido_ataque_area(self, poder_nome, maximo):
        print("O poder " + poder_nome + " pode acertar até " + maximo + " alvos")

    def poder_escolhido_ataque_unico(self, poder_nome):
        print("O poder " + poder_nome + " pode acertar um alvo")

    def poder_escolhido_cura_unica(self, poder_nome):
        print("O poder " + poder_nome + " pode curar um aliado")

    def escolher_alvo_area(self, escolhidos, maximo, opcoes_alvos):
        return input("Selecione um alvo:\n" + opcoes_alvos + "\nAlvos selecionados[" + escolhidos + "/" + maximo + "]")

    def escolher_alvo_unico(self, opcoes_alvos):
        return input("Selecione um alvo:\n" + opcoes_alvos)
