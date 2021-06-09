from typing import Tuple, Set, Optional
from dataclasses import dataclass

@dataclass
class PercepcoesJogador():
    '''Coloque aqui atributos que descrevam as percepções possíveis de
    mundo por parte do agente jogador
    
    Vide documentação sobre dataclasses em python.
    '''    
    pos_bolinhas: Set[Tuple[int,int]]
    dimensoes: Tuple[int, int] = (7,7)
    mensagem_jogo: Optional[str] = None