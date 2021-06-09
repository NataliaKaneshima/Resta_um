from enum import Enum
from dataclasses import dataclass

class AcoesJogador(Enum):
    MOVER_BOLINHA = 'MoverBolinha'

class DirecaoMoverBolinha(Enum):
    DIREITA = 'Direita'
    ESQUERDA = 'Esquerda'
    CIMA = 'Cima'
    BAIXO = 'Baixo'

@dataclass
class AcaoJogador():
    tipo: str
    parametros: tuple = tuple()

    @classmethod
    def mover_bolinha(cls, x: int, y: int, direcao: DirecaoMoverBolinha) -> 'AcaoJogador':
        return cls(AcoesJogador.MOVER_BOLINHA, (x, y, direcao))