import math
import numpy as np
import itertools
from multiprocessing import Pool


def combinatoire(a,b):
    comb = math.factorial(a)/(math.factorial(b)*math.factorial(a-b))
    return comb
def HyperGemotricDistribution(N, B, W, k):
    FirstTerm = combinatoire(B,k)
    SecondTerm = combinatoire(N-B,W -k )
    ThirdTerm = combinatoire(N, W)
    prob = FirstTerm * SecondTerm /ThirdTerm
    return prob
def main(rate):
    N = 120
    B = 4
    L = 5
    W = N//L
    combinations = itertools.product(range(B + 1), repeat=L)
    b = [np.array(tuple) for tuple in combinations if sum(tuple) == B and max(tuple) <= W]

    print(b)
    ProbPath = math.pow(1/W, L)
    summation = 0
    for i in range(len(b)):
        prod = 1
        ST = B
        FT = N
        for j in range(L- 1):
            prod *= b[i][j] * HyperGemotricDistribution(FT, ST, W, b[i][j])
            FT = FT - W
            ST = ST - b[i][j]

        prod *= b[i][-1]
        summation += prod
    PrF = ProbPath * summation
    return PrF
if __name__ == "__main__":
    nbsims = 1
    p = Pool(processes=1)
    p = Pool(maxtasksperchild=1)
    param = [2]
    result = p.map(main,param, chunksize=1)
    print("PrF", result)