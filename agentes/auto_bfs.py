import time
from typing import Tuple

from percepcoes import PercepcoesJogador
from acoes import AcaoJogador, DirecaoMoverBolinha

from .abstrato import AgenteAbstrato
from .problemas.resta_um import ProblemaRestaUm
from .buscadores.busca import busca_arvore_bfs


class AgenteAutomaticoBfs(AgenteAbstrato):

    def __init__(self) -> None:
        super().__init__()

        self.problema: ProblemaRestaUm = None
        self.solucao: list = None

    def adquirirPercepcao(self, percepcao_mundo: PercepcoesJogador):
        """ Inspeciona a disposicao dos elementos no objeto de visao."""
        AgenteAutomaticoBfs.desenhar_tabuleiro(percepcao_mundo)

        if not self.solucao:
            self.problema = ProblemaRestaUm()  # TODO: # percepcao_mundo)
        
    def escolherProximaAcao(self):
        if not self.solucao:
            no_solucao = busca_arvore_bfs(self.problema)
            self.solucao = no_solucao.caminho_acoes()
            print(len(self.solucao), self.solucao)
            if not self.solucao:
                raise Exception("Agente BFS não encontrou solução.")
        
        acao = self.solucao.pop(0)
        print(f"Próxima ação é {acao}.")
        time.sleep(2)

        x, y, d = AgenteAutomaticoBfs.traduzir_acao_jogo(acao)
        return AcaoJogador.mover_bolinha(x, y, d)
    
    @staticmethod
    def traduzir_acao_jogo(acao):
        direcoes = {
            'direita': DirecaoMoverBolinha.DIREITA,
            'esquerda': DirecaoMoverBolinha.ESQUERDA,
            'cima': DirecaoMoverBolinha.CIMA,
            'baixo': DirecaoMoverBolinha.BAIXO
        }

        x, y = acao.bolinha.x, acao.bolinha.y
        d = direcoes[acao.direcao]
        return x, y, d

    @staticmethod
    def desenhar_tabuleiro(percepcao_mundo: PercepcoesJogador):
        """Escreve na tela para o usuário saber o que seu agente 
        está percebendo.
        """
        print("\nTabuleiro após a última jogada.")

        linhas, colunas = percepcao_mundo.dimensoes
        start_linha, stop_linha = linhas//2, -1 * linhas//2
        start_coluna, stop_coluna = -1 * (colunas//2), colunas//2 + 1

        print("+-3210123+")
        for linha in range(start_linha, stop_linha, -1):
            print_linha = f'{abs(linha)} '
            for coluna in range(start_coluna, stop_coluna, 1):
                if (coluna, linha) in percepcao_mundo.pos_bolinhas:
                    print_linha += 'o'
                else:
                    print_linha += '.'
        
            print(print_linha)
        print('-')

        if percepcao_mundo.mensagem_jogo:
            print(f'Mensagem do jogo: {percepcao_mundo.mensagem_jogo}')
