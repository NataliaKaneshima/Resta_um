from typing import Sequence, Set
from dataclasses import dataclass


@dataclass
class Bolinha:
    x: int
    y: int

    def __hash__(self) -> int:
        return hash(self.x) + hash(self.y)
    
    def __str__(self) -> str:
        return f'B({self.x},{self.y})'


@dataclass
class EstadoRestaUm:
    tabuleiro: Set[Bolinha]


@dataclass
class Mover:
    bolinha: Bolinha
    direcao: str

    def __str__(self) -> str:
        return f'Mover({self.bolinha},{self.direcao})'


class ProblemaRestaUm:

    @staticmethod
    def estado_inicial(*args,**kwargs) -> EstadoRestaUm:
        niveis = {
            'completo': EstadoRestaUm({ 
                Bolinha(-1,3), Bolinha(0,3), Bolinha(1,3),
                Bolinha(-1,2), Bolinha(0,2), Bolinha(1,2),
                Bolinha(-3,1),Bolinha(-2,1),Bolinha(-1,1),Bolinha(0,1),Bolinha(1,1),Bolinha(2,1),Bolinha(3,1),
                Bolinha(-3,0),Bolinha(-2,0),Bolinha(-1,0),Bolinha(1,0),Bolinha(2,0),Bolinha(3,0),
                Bolinha(-3,-1),Bolinha(-2,-1),Bolinha(-1,-1),Bolinha(0,-1),Bolinha(1,-1),Bolinha(2,-1),Bolinha(3,-1),
                Bolinha(-1,-2), Bolinha(0,-2), Bolinha(1,-2),
                Bolinha(-1,-3), Bolinha(0,-3), Bolinha(1,-3)
            }),
            'cruz-simples': EstadoRestaUm({
                Bolinha(0,1),
                Bolinha(-1,0), Bolinha(0,0), Bolinha(1,0),
                Bolinha(0,-1),
                Bolinha(0,-2)
            })
        }
        return niveis[kwargs.get('nivel', 'completo')]

    @staticmethod
    def acoes(estado: EstadoRestaUm) -> Sequence[Mover]:
        acoes_possiveis = list()
        for bolinha in estado.tabuleiro:
            x, y = bolinha.x, bolinha.y

            if Bolinha(x+1,y) in estado.tabuleiro and Bolinha(x+2,y) not in estado.tabuleiro:
                x_max = 3 if abs(y) < 2 else 1
                if x+2 <= x_max:
                    acoes_possiveis.append(Mover(bolinha, 'direita'))
            
            if Bolinha(x-1,y) in estado.tabuleiro and Bolinha(x-2,y) not in estado.tabuleiro:
                x_min = -3 if abs(y) < 2 else -1
                if x-2 >= x_min:
                    acoes_possiveis.append(Mover(bolinha, 'esquerda'))
            
            if Bolinha(x,y+1) in estado.tabuleiro and Bolinha(x,y+2) not in estado.tabuleiro:
                y_max = 3 if abs(x) < 2 else 1
                if y+2 <= y_max:
                    acoes_possiveis.append(Mover(bolinha, 'cima'))
            
            if Bolinha(x,y-1) in estado.tabuleiro and Bolinha(x,y-2) not in estado.tabuleiro:
                y_min = -3 if abs(x) < 2 else -1
                if y-2 >= y_min:
                    acoes_possiveis.append(Mover(bolinha, 'baixo'))
        
        return acoes_possiveis
    
    @staticmethod
    def resultado(estado: EstadoRestaUm, acao: Mover) -> EstadoRestaUm:
        estado_resultante = EstadoRestaUm(set(estado.tabuleiro))
        x, y = acao.bolinha.x, acao.bolinha.y
        
        estado_resultante.tabuleiro.discard(acao.bolinha)
        if acao.direcao == 'cima':
            estado_resultante.tabuleiro.discard(Bolinha(x, y+1))
            estado_resultante.tabuleiro.add(Bolinha(x, y+2))
        
        elif acao.direcao == 'baixo':
            estado_resultante.tabuleiro.discard(Bolinha(x, y-1))
            estado_resultante.tabuleiro.add(Bolinha(x, y-2))

        elif acao.direcao == 'direita':
            estado_resultante.tabuleiro.discard(Bolinha(x+1, y))
            estado_resultante.tabuleiro.add(Bolinha(x+2, y))
        
        elif acao.direcao == 'esquerda':
            estado_resultante.tabuleiro.discard(Bolinha(x-1, y))
            estado_resultante.tabuleiro.add(Bolinha(x-2, y))
        
        else:
            raise ValueError("Movimento especificado inválido, cheater!")
        
        return estado_resultante
    
    @staticmethod
    def teste_objetivo(estado: EstadoRestaUm) -> bool:
        return len(estado.tabuleiro) == 1
    
    @staticmethod
    def avaliacao(estado: EstadoRestaUm) -> int:
        return len(estado.tabuleiro)

    @staticmethod
    def custo(inicial: EstadoRestaUm, acao: Mover, 
              resultante: EstadoRestaUm) -> int:
        """Custo em quantidade de jogadas"""
        return 1
