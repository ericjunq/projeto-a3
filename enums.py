from enum import Enum

class TipoRequestEnum(str, Enum):
    reclamacao = 'reclamacao'
    sugestao = 'sugestao'
    
class StatusReclamacao(str, Enum):
    concluida = "Concluída"
    em_andamento = "Em Andamento"
    nao_realizada = "Não Realizada"