# bacteria.py mejorado con mutación controlada y corrección de overflow
import copy
import math
from multiprocessing import Manager, Pool
from evaluadorBlosum import evaluadorBlosum
import numpy
from fastaReader import fastaReader
import random
from copy import deepcopy
import concurrent.futures

class bacteria():

    def __init__(self, numBacterias):
        manager = Manager()
        self.blosumScore = manager.list(range(numBacterias))
        self.tablaAtract = manager.list(range(numBacterias))
        self.tablaRepel = manager.list(range(numBacterias))
        self.tablaInteraction = manager.list(range(numBacterias))
        self.tablaFitness = manager.list(range(numBacterias))
        self.granListaPares = manager.list(range(numBacterias))
        self.NFE = manager.list(range(numBacterias))

    def resetListas(self, numBacterias):
        manager = Manager()
        self.blosumScore = manager.list(range(numBacterias))
        self.tablaAtract = manager.list(range(numBacterias))
        self.tablaRepel = manager.list(range(numBacterias))
        self.tablaInteraction = manager.list(range(numBacterias))
        self.tablaFitness = manager.list(range(numBacterias))
        self.granListaPares = manager.list(range(numBacterias))
        self.NFE = manager.list(range(numBacterias))

    def cuadra(self, numSec, poblacion):
        for i in range(len(poblacion)):
            bacterTmp = list(poblacion[i])
            maxLen = max(len(seq) for seq in bacterTmp)
            for t in range(numSec):
                gap_count = maxLen - len(bacterTmp[t])
                if gap_count > 0:
                    bacterTmp[t].extend(["-"] * gap_count)
            poblacion[i] = tuple(bacterTmp)

    def tumbo(self, numSec, poblacion, numGaps):
        for i in range(len(poblacion)):
            bacterTmp = list(poblacion[i])
            for j in range(numGaps):
                seqnum = random.randint(0, len(bacterTmp)-1)
                pos = random.randint(0, len(bacterTmp[seqnum]))
                part1 = bacterTmp[seqnum][:pos]
                part2 = bacterTmp[seqnum][pos:]
                temp = part1 + ["-"] + part2
                bacterTmp[seqnum] = temp
            poblacion[i] = tuple(bacterTmp)

    def creaGranListaPares(self, poblacion):
        for i in range(len(poblacion)):
            pares = []
            bacterTmp = list(poblacion[i])
            for j in range(len(bacterTmp[0])):
                column = self.getColumn(bacterTmp, j)
                pares += self.obtener_pares_unicos(column)
            self.granListaPares[i] = pares

    def evaluaFila(self, fila, num):
        evaluador = evaluadorBlosum()
        score = sum(evaluador.getScore(par[0], par[1]) for par in fila)
        self.blosumScore[num] = score

    def evaluaBlosum(self):
        with Pool() as pool:
            args = [(copy.deepcopy(self.granListaPares[i]), i) for i in range(len(self.granListaPares))]
            pool.starmap(self.evaluaFila, args)

    def getColumn(self, bacterTmp, colNum):
        return [bacterTmp[i][colNum] for i in range(len(bacterTmp))]

    def obtener_pares_unicos(self, columna):
        pares_unicos = set()
        for i in range(len(columna)):
            for j in range(i+1, len(columna)):
                par = tuple(sorted([columna[i], columna[j]]))
                pares_unicos.add(par)
        return list(pares_unicos)

    def compute_diff(self, args):
        indexBacteria, otherBlosumScore, selfScore, d, w = args
        diff = (selfScore[indexBacteria] - otherBlosumScore) ** 2.0
        self.NFE[indexBacteria] += 1
        exp_input = min(w * diff, 700)  # corrección para evitar overflow
        return d / (1 + diff)

    def compute_cell_interaction(self, indexBacteria, d, w, atracTrue):
        with Pool() as pool:
            args = [(indexBacteria, other, self.blosumScore, d, w) for other in self.blosumScore]
            results = pool.map(self.compute_diff, args)

        total = sum(results)
        if atracTrue:
            self.tablaAtract[indexBacteria] = total
        else:
            self.tablaRepel[indexBacteria] = total

    def creaTablaAtract(self, poblacion, d, w):
        for indexBacteria in range(len(poblacion)):
            self.compute_cell_interaction(indexBacteria, d, w, True)

    def creaTablaRepel(self, poblacion, d, w):
        for indexBacteria in range(len(poblacion)):
            self.compute_cell_interaction(indexBacteria, d, w, False)

    def creaTablasAtractRepel(self, poblacion, dAttr, wAttr, dRepel, wRepel):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.submit(self.creaTablaAtract, poblacion, dAttr, wAttr)
            executor.submit(self.creaTablaRepel, poblacion, dRepel, wRepel)

    def creaTablaInteraction(self):
        for i in range(len(self.tablaAtract)):
            self.tablaInteraction[i] = self.tablaAtract[i] + self.tablaRepel[i]

    def creaTablaFitness(self):
        for i in range(len(self.tablaInteraction)):
            self.tablaFitness[i] = self.blosumScore[i] + self.tablaInteraction[i]

    def getNFE(self):
        return sum(self.NFE)

    def obtieneBest(self, globalNFE):
        bestIdx = max(range(len(self.tablaFitness)), key=lambda i: self.tablaFitness[i])
        print("-------------------   Best: ", bestIdx, " Fitness: ", self.tablaFitness[bestIdx],
              "BlosumScore ", self.blosumScore[bestIdx], "Interaction: ", self.tablaInteraction[bestIdx],
              "NFE: ", globalNFE)
        return bestIdx, self.tablaFitness[bestIdx]

    def mutar(self, bacterium):
        bacterium = list(deepcopy(bacterium))
        seq_idx = random.randint(0, len(bacterium) - 1)
        seq = bacterium[seq_idx]
        if len(seq) > 1:
            op = random.choice(['insert', 'delete'])
            pos = random.randint(0, len(seq) - 1)
            if op == 'insert':
                seq.insert(pos, '-')
            elif op == 'delete' and seq[pos] == '-':
                del seq[pos]
        bacterium[seq_idx] = seq
        return tuple(bacterium)

    def replaceWorst(self, poblacion, best):
        worst = min(range(len(self.tablaFitness)), key=lambda i: self.tablaFitness[i])
        nueva_bacteria = self.mutar(poblacion[best])
        poblacion[worst] = nueva_bacteria
