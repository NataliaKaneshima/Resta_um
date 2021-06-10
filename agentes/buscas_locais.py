import random
from itertools import islice
from typing import Iterable, Optional, List

from problemas.resta_um import ProblemaRestaUm, EstadoRestaUm

def subida_encosta(estado_inicial: EstadoRestaUm) -> EstadoRestaUm:
    melhor_atual = estado_inicial
    while True:
        acoes = melhor_atual.acoes
        melhor_adjacente = min(acoes, key=lambda estado: estado.avaliacao)
        
        if melhor_adjacente.avaliacao < melhor_atual.avaliacao:
            melhor_atual = melhor_adjacente
        else:
            return melhor_atual

def subida_encosta_repetida(gerador: Iterable[EstadoRestaUm],
                            repeticoes: Optional[int] = None) -> EstadoRestaUm:
    for tentativa, estado_gerado in enumerate(islice(gerador, repeticoes), start=1):
        print(f'Iniciando tentativa {tentativa}...')
        solucao = subida_encosta(estado_gerado)
        if solucao.teste_objetivo:
            return solucao


def subida_feixe_local(estados_iniciais: List[EstadoRestaUm]) -> EstadoRestaUm:
    k = len(estados_iniciais)
    k_atuais = estados_iniciais
    while True:
        k_acoes = list()
        for k_atual in k_atuais:
            k_acoes += list(k_atual.acoes)
        k_acoes.sort(key=lambda estado: estado.avaliacao)
        
        if k_acoes[0].avaliacao < k_atuais[0].avaliacao:
            k_atuais = k_acoes[:k]
        else:
            return k_atuais[0]


def subida_feixe_local_gen(generator: Iterable[EstadoRestaUm], k: int) -> EstadoRestaUm:
    estados_iniciais = [estado for estado in islice(generator, k)]
    return subida_feixe_local(estados_iniciais)