from typing import Optional


class Cidade:
    nome: str
    pais: str
    latitude: float
    longitude: float
    entradas: list
    temperaturaMedia: Optional[float]

    def __init__(self, nome: str, pais: str, latitude: float, longitutde: float):
        self.nome = nome
        self.pais = pais
        self.latitude = latitude
        self.longitude = longitutde
        self.entradas = []
        self.temperaturaMedia = None

    def __str__(self):
        return f'{self.nome} - {self.pais} com coordenadas ({self.longitude} - {self.latitude})'
