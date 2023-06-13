from controllers.controller_personagem import ControllerPersonagem
from exceptions.exceptions import DuplicadoException
from models.classe import Classe
from models.npc import Npc
from models.poder import Poder


class ControllerNpc(ControllerPersonagem):
    def cadastrar(self, nome: str, classe: Classe, poderes: list[Poder] = []):
        """
        Adiciona um Npc na lista de personagens
        :param nome: identicador do Npc
        :param classe: Classe possui os atributos principais do personagem
        :param poderes: Habilidades que o Npc pode utilizar
        :return: o Npc cadastrado
        """
        npc = Npc(nome, classe, poderes)

        if super().get_by_name(nome):
            raise DuplicadoException('Não foi possivel criar o npc pois ja existe um com o mesmo nome')

        super().personagens.append(npc)

        return npc
