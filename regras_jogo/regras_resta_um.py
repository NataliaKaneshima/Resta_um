from typing import Tuple

from .regras_abstratas import AbstractRegrasJogo
from .personagens import Personagens
from percepcoes import PercepcoesJogador
from acoes import AcoesJogador, DirecaoMoverBolinha

class RegrasRestaUm(AbstractRegrasJogo):
    """ Interface mínima para implementar um jogo interativo e modular. Não
    tente instanciar objetos dessa classe, ela deve ser herdada e seus métodos
    abstratos sobrecarregados.
    """

    def __init__(self) -> None:
        super().__init__()
        tabuleiro_completo = { 
                (-1,3), (0,3), (1,3),
                (-1,2), (0,2), (1,2),
                (-3,1),(-2,1),(-1,1),(0,1),(1,1),(2,1),(3,1),
                (-3,0),(-2,0),(-1,0),(1,0),(2,0),(3,0),
                (-3,-1),(-2,-1),(-1,-1),(0,-1),(1,-1),(2,-1),(3,-1),
                (-1,-2), (0,-2), (1,-2),
                (-1,-3), (0,-3), (1,-3)
            }

        self.tabuleiro = tabuleiro_completo
        self.id_personagens = {Personagens.JOGADOR_RESTA_UM: 0}
        self.acoes_personagens = {0: None}
        self.msg_jogador = None

    @property
    def qtde_bolinhas(self) -> int:
        return len(self.tabuleiro)
    
    @property
    def bolinhas_adjacentes(self) -> int:
        adjacentes = 0
        for bolinha in self.tabuleiro:
            x, y = bolinha
            if (x+1, y) in self.tabuleiro:
                adjacentes += 1
            if (x-1, y) in self.tabuleiro:
                adjacentes += 1
            if (x, y+1) in self.tabuleiro:
                adjacentes += 1
            if (x, y-1) in self.tabuleiro:
                adjacentes += 1
            
            # adjacentes_bolinha = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
            # adjacentes += sum(1 if adj in self.tabuleiro else 0 
            #     for adj in adjacentes_bolinha)
        
        return adjacentes

    def registrarAgentePersonagem(self, personagem):
        """ Cria ou recupera id de um personagem agente.
        """
        return self.id_personagens[personagem]
    
    def isFim(self):
        """ Boolean indicando fim de jogo em True.
        """
        return self.qtde_bolinhas == 1 or self.bolinhas_adjacentes == 0

    def gerarCampoVisao(self, id_agente):
        """ Retorna um PercepcoesJogador para ser consumido por um agente
        específico. Objeto deve conter apenas descrição de elementos visíveis
        para este agente.

        PercepcoesJogador é um objeto imutável ou uma cópia do jogo, de forma que
        sua manipulação direta não tem nenhum efeito no mundo de jogo real.
        """
        percepcoes_jogador = PercepcoesJogador(
            pos_bolinhas=set(self.tabuleiro),
            dimensoes=(7, 7),
            mensagem_jogo=self.msg_jogador)

        self.msg_jogador = None
        return percepcoes_jogador

    def registrarProximaAcao(self, id_agente, acao) -> None:
        """ Informa ao jogo qual a ação de um jogador especificamente.
        Neste momento, o jogo ainda não é transformado em seu próximo estado,
        isso é feito no método de atualização do mundo.
        """
        self.acoes_personagens[id_agente] = acao
    
    def atualizarEstado(self, diferencial_tempo):
        """ Apenas neste momento o jogo é atualizado para seu próximo estado
        de acordo com as ações de cada jogador registradas anteriormente.
        """
        acao_jogador = self.acoes_personagens[
            self.id_personagens[Personagens.JOGADOR_RESTA_UM]]
        if acao_jogador.tipo == AcoesJogador.MOVER_BOLINHA:
            x, y, direcao = acao_jogador.parametros

            if (x, y) in self.tabuleiro:
                x_mov, y_mov = self.decodificar_direcao(direcao)

                peca_adjacente = (x + x_mov, y + y_mov)
                espaco_pos_adjacente = (x + x_mov*2, y + y_mov*2)
                if self.is_jogada_valida(peca_adjacente, espaco_pos_adjacente):
                    self.tabuleiro.discard(peca_adjacente)
                    self.tabuleiro.discard((x,y))
                    self.tabuleiro.add(espaco_pos_adjacente)
                else:
                    self.msg_jogador = f'Direção especificada para movimento não é possível.'
            else:
                self.msg_jogador = f'Não há bolinha na coordenada especificada.'
        else:
            self.msg_jogador = f'Ação especificada inválida.'

        return
    
    def terminarJogo(self):
        """ Faz procedimentos de fim de jogo, como mostrar placar final,
        gravar resultados, etc...
        """
        return
    
    def is_jogada_valida(self, peca_adjacente: Tuple[int, int],
                          espaco_pos_adjacente: Tuple[int, int]) -> bool:
        return peca_adjacente in self.tabuleiro \
            and espaco_pos_adjacente not in self.tabuleiro \
            and RegrasRestaUm.is_espaco_tabuleiro_valido(*espaco_pos_adjacente)

    @staticmethod
    def is_espaco_tabuleiro_valido(x: int, y: int) -> bool:
        """Verifica se (x, y) é um espaço válido em um tabuleiro de Resta Um
        regular 7x7, onde (0,0) é o meio do tabuleiro.
        """
        return not ((abs(x) > 1 and abs(y) > 1) or abs(x) > 3 or abs(y) > 3)

    @staticmethod
    def decodificar_direcao(direcao) -> Tuple[int, int]:
        if direcao == DirecaoMoverBolinha.BAIXO:
            return (0, -1)
        elif direcao == DirecaoMoverBolinha.CIMA:
            return (0, 1)
        elif direcao == DirecaoMoverBolinha.DIREITA:
            return (1, 0)
        elif direcao == DirecaoMoverBolinha.ESQUERDA:
            return (-1, 0)
        else:
            raise ValueError(f"Direção {direcao} é inválida.")

def construir_jogo(*args,**kwargs):
    """ Método factory para uma instância RegrasJogo arbitrária, de acordo com os
    parâmetros. Pode-se mudar à vontade a assinatura do método.
    """
    return RegrasRestaUm()