class DuplicadoException(Exception):
    pass


class NaoEncontradoException(Exception):
    pass


class CombateAcabou(Exception):
    pass


class VitoriaCombateAcabou(CombateAcabou):
    pass


class DerrotaCombateAcabou(CombateAcabou):
    pass
