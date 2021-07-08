import numpy as np
import random

def XRD_New(ListCascades):
    groups_list = []
    group1 = []
    group1.append(ListCascades[1])
    group1.append(ListCascades[2])
    group1.append(ListCascades[3])
    groups_list.append(group1)

    group2 = []
    group2.append(ListCascades[1])
    group2.append(ListCascades[4])
    group2.append(ListCascades[5])
    groups_list.append(group2)

    group3 = []
    group3.append(ListCascades[2])
    group3.append(ListCascades[4])
    group3.append(ListCascades[6])
    groups_list.append(group3)

    group4 = []
    group4.append(ListCascades[3])
    group4.append(ListCascades[5])
    group4.append(ListCascades[6])
    groups_list.append(group4)
    return groups_list
def Capacity( C, nbrNodes):
    arr = []
    for i in range(nbrNodes):
        arr.append(C)
    return arr
def Weights (Number_layer, Number_Mix_Per_Layer):
    probability = []
    for i in range(Number_layer):
        probabTem = []
        for j in range(Number_Mix_Per_Layer):
            probabTem.append((1) / (Number_Mix_Per_Layer))
        probability.append(probabTem)
    return probability

def flip(nbr1, nbr2):
    if nbr1 == nbr2:
        return 1
    elif nbr1 == 0.0 and nbr2 == 0.0:
        return None
    elif nbr1 > nbr2 and nbr2 != 0.0:
        return nbr1 / nbr2
    elif nbr2 > nbr1 and nbr1 != 0.0:
        return nbr2 / nbr1
    elif (nbr1 > nbr2 and nbr2 == 0.0) or (nbr2 > nbr1 and nbr1 == 0.0):
        return 1000


def Epsilon(s):
    a = [[10, 10, 10, 10, 10, 10, 100, 10, 10, 10, 10, 10, 10, 10, 10, 100, 10, 10, 10, 10, 10, 10, 10, 10, 10, 500, 10,
          10, 10, 10, 10, 10, 10],
         [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 500, 10, 10, 100, 10, 10,
          10, 10, 10, 10, 10, 10],
         [500, 100, 100, 100, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
          10, 10, 10, 10, 10, 10, 10]]
    return a


def OptimizedPositions(s, nbr):
    k = (len(s) // nbr - 2) * nbr  # slice limit

    s.sort(reverse=True)
    a = []
    for j in range(0, nbr - 1):
        a.append(s[j + 1:k:nbr])
    a.append(s[:k:nbr])
    sum_a = list(map(sum, a))
    for x in s[k:]:
        i = sum_a.index(min(sum_a))
        sum_a[i] += x
        a[i].append(x)
    return a
def XRD(Client_i, arrayCascades):
    random1 = random.randint(0, len(arrayCascades) - 1)
    random2 = random.randint(0, len(arrayCascades) - 1)
    l = [random1, random2]
    Cascade1 = arrayCascades[random1]
    Cascade2 = arrayCascades[random2]
    Cascade = []
    Cascade.append(Cascade1)
    Cascade.append(Cascade2)
    if Client_i < 25:
        Cascade = []
        Cascade.append(arrayCascades[0])
        Cascade.append(arrayCascades[1])
        Cascade.append(arrayCascades[2])
        Cascade.append(arrayCascades[3])
    elif Client_i >= 25 and Client_i < 50:
        Cascade = []
        Cascade.append(arrayCascades[1])
        Cascade.append(arrayCascades[4])
        Cascade.append(arrayCascades[5])
        Cascade.append(arrayCascades[6])
    elif Client_i >= 50 and Client_i < 75:
        Cascade = []
        Cascade.append(arrayCascades[3])
        Cascade.append(arrayCascades[2])
        Cascade.append(arrayCascades[5])
        Cascade.append(arrayCascades[7])
    else:
        Cascade = []
        Cascade.append(arrayCascades[3])
        Cascade.append(arrayCascades[6])
        Cascade.append(arrayCascades[7])
        Cascade.append(arrayCascades[8])
    return Cascade

def PositionErrorRate(s):
    s = sorted(s, reverse=True)
    a = [[], [], []]
    sum_a = [0, 0, 0]
    for x in s:
        i = sum_a.index(min(sum_a))
        sum_a[i] += x
        a[i].append(x)
    a[1].sort()
    a[2][a[0].index(min(a[2]))], a[1][a[1].index(a[1][-2])] = a[1][-2], min(a[2])
    return a


def RandomPosition(s):
    temp = s
    a = []
    nbr = int(len(temp) / 3)
    a1 = random.sample(temp, k=nbr)
    for i in range(len(a1)):
        temp.remove(a1[i])
    a2 = random.sample(temp, k=nbr)
    for i in range(len(a2)):
        temp.remove(a2[i])
    a3 = temp
    a.append(a1)
    a.append(a2)
    a.append(a3)
    return a
