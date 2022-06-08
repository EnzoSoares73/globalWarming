from datetime import datetime

from Cidade import Cidade


class Entrada:
    data: datetime
    cidade: Cidade
    temperaturaMedia: float
    incertezaMedia: float

    def __init__(self, data: datetime, cidade: Cidade, temperaturaMedia: float, incertezaMedia: float):
        self.data = data
        self.cidade = cidade
        self.temperaturaMedia = temperaturaMedia
        self.incertezaMedia = incertezaMedia
