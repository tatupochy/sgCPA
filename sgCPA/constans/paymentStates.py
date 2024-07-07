from enum import Enum

class StateEnum(Enum):
    Pendiente = 'pending'
    Pagado =   'paid'
    Vencido =  'overdue'