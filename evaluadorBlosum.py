# evaluadorBlosum.py
import blosum as bl

class evaluadorBlosum():
    def __init__(self):
        matrix = bl.BLOSUM(62)
        self.matrix = matrix

    def getScore(self, A, B):
        if A == "-" or B == "-":
            return -8
        return self.matrix[A][B]