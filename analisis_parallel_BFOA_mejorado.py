# analisis_parallel_BFOA_mejorado.py
from copy import deepcopy
from multiprocessing import Manager, freeze_support
import time
from bacteria import bacteria
from fastaReader import fastaReader
import csv

if __name__ == "__main__":
    freeze_support()
    numeroDeBacterias = 4
    iteraciones = 3
    tumbo = 2
    dAttr = 0.1
    wAttr = 0.002
    hRep = dAttr
    wRep = 0.001

    reader = fastaReader()
    secuencias = [list(seq) for seq in reader.seqs]
    numSec = len(secuencias)

    resultados = []

    for corrida in range(30):
        manager = Manager()
        poblacion = manager.list(range(numeroDeBacterias))

        def poblacionInicial():
            for i in range(numeroDeBacterias):
                bacterium = [list(seq) for seq in secuencias]
                poblacion[i] = list(bacterium)

        operadorBacterial = bacteria(numeroDeBacterias)
        globalNFE = 0
        veryBest = [None, float('-inf'), None]

        start_time = time.time()
        poblacionInicial()

        for it in range(iteraciones):
            operadorBacterial.tumbo(numSec, poblacion, tumbo)
            operadorBacterial.cuadra(numSec, poblacion)
            operadorBacterial.creaGranListaPares(poblacion)
            operadorBacterial.evaluaBlosum()
            operadorBacterial.creaTablasAtractRepel(poblacion, dAttr, wAttr, hRep, wRep)
            operadorBacterial.creaTablaInteraction()
            operadorBacterial.creaTablaFitness()

            globalNFE += operadorBacterial.getNFE()
            bestIdx, bestFitness = operadorBacterial.obtieneBest(globalNFE)

            if bestFitness > veryBest[1]:
                veryBest = [bestIdx, bestFitness, deepcopy(poblacion[bestIdx])]

            operadorBacterial.replaceWorst(poblacion, veryBest[0])
            operadorBacterial.resetListas(numeroDeBacterias)

        tiempo_total = time.time() - start_time
        resultados.append({
            "corrida": corrida + 1,
            "fitness": veryBest[1],
            "tiempo": tiempo_total,
            "interaccion": operadorBacterial.tablaInteraction[veryBest[0]],
            "blosum": operadorBacterial.blosumScore[veryBest[0]]
        })

    with open("resultados_BFOA_mejorado.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=resultados[0].keys())
        writer.writeheader()
        writer.writerows(resultados)

    print("¡Análisis de desempeño del algoritmo mejorado completado! Resultados guardados en 'resultados_BFOA_mejorado.csv'")
