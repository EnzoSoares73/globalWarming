import math
from datetime import datetime
from typing import Optional

import matplotlib.cm
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from mpl_toolkits.basemap import Basemap

from Cidade import Cidade
from entrada import Entrada


def main() -> None:
    listaCidades: list = lerEntradas()
    gerarMapa(listaCidades)
    plotaIncerteza(listaCidades)
    plotaTemperatura(listaCidades)


def lerEntradas() -> list:
    listaCidades: list = []
    with open('GlobalLandTemperaturesByCity.csv', encoding="utf-8") as csvfile:
        dataFrame = pd.read_csv(csvfile)
        print(f'A dataFrame tem {dataFrame.shape[0]} linhas.')
        for i in range(dataFrame.shape[0]):
            cidade = contemCidade(listaCidades, dataFrame.iloc[i]['City'])
            if cidade is None:
                cidade = Cidade(dataFrame.iloc[i]['City'],
                                dataFrame.iloc[i]['Country'],
                                textoParaFloat(dataFrame.iloc[i]['Latitude']),
                                textoParaFloat(dataFrame.iloc[i]['Longitude']))
                print(f'Cidade {cidade} adicionada.')

                entrada = Entrada(datetime.strptime(dataFrame.iloc[i]['dt'], '%Y-%m-%d'),
                                  cidade,
                                  dataFrame.iloc[i]['AverageTemperature'],
                                  dataFrame.iloc[i]['AverageTemperatureUncertainty'])
                cidade.entradas.append(entrada)
                listaCidades.append(cidade)
            else:
                entrada = Entrada(datetime.strptime(dataFrame.iloc[i]['dt'], '%Y-%m-%d'),
                                  cidade,
                                  dataFrame.iloc[i]['AverageTemperature'],
                                  dataFrame.iloc[i]['AverageTemperatureUncertainty'])
                cidade.entradas.append(entrada)

        print(f'Foram analisadas {len(listaCidades)} cidades.')

    for cidade in listaCidades:
        soma: float = 0
        count: int = 0
        for entrada in cidade.entradas:
            if entrada.temperaturaMedia is not None and not math.isnan(entrada.temperaturaMedia):
                soma += entrada.temperaturaMedia
                count += 1
        cidade.temperaturaMedia = soma / count

    return listaCidades


def textoParaFloat(entrada: str) -> float:
    entrada = entrada.replace("N", "")
    entrada = entrada.replace("E", "")
    if "S" in entrada or "W" in entrada:
        entrada = entrada.replace("S", "")
        entrada = entrada.replace("W", "")
        return -float(entrada)
    return float(entrada)


def plotaIncerteza(listaCidades: list) -> None:
    plt.figure(figsize=(10, 10), dpi=80)
    for cidade in listaCidades:
        listaDatas: list = []
        listaIncerteza: list = []
        for entrada in cidade.entradas:
            listaDatas.append(entrada.data)
            listaIncerteza.append(entrada.incertezaMedia)
        plt.scatter(listaDatas, listaIncerteza, s=0.4)
    plt.show()


def gerarMapa(listaCidades: list) -> None:
    map = Basemap(projection='mill')
    plt.figure(figsize=(10, 10), dpi=80)
    map.drawcountries()
    map.drawparallels(np.arange(-90, 90, 30), labels=[1, 0, 0, 0])
    map.drawmeridians(np.arange(map.lonmin, map.lonmax + 30, 60), labels=[0, 0, 0, 1])
    map.drawmapboundary(fill_color='aqua')
    map.fillcontinents(color='yellow', lake_color='aqua')

    map.scatter(list(cidade.longitude for cidade in listaCidades), list(cidade.latitude for cidade in listaCidades),
                c=list(cidade.temperaturaMedia for cidade in listaCidades), marker='o', zorder=50, latlon=True,
                cmap=matplotlib.cm.get_cmap("coolwarm"))

    plt.show()


def plotaTemperatura(listaCidades: list) -> None:
    plt.figure(figsize=(10, 10), dpi=80)
    for cidade in listaCidades:
        ano: int = int(min(list(entrada.data.year for entrada in cidade.entradas)))
        lista: list = []
        dicionario: dict = {}
        for entrada in cidade.entradas:
            if not math.isnan(entrada.temperaturaMedia):
                if ano == entrada.data.year:
                    lista.append(entrada.temperaturaMedia)
                else:
                    dicionario[ano] = np.std(lista)
                    lista.clear()
                    ano = entrada.data.year

        plt.plot(list(int(key) for key in dicionario.keys()),
                 np.poly1d(np.polyfit(list(int(key) for key in dicionario.keys()), list(dicionario.values()), 1))(
                     np.unique(list(int(key) for key in dicionario.keys()))))
    plt.show()


def contemCidade(listaCidades: list, nomeCidade: str) -> Optional[Cidade]:
    for cidade in listaCidades:
        if cidade.nome == nomeCidade:
            return cidade
    return None


if __name__ == '__main__':
    main()
