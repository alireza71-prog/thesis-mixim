import random
import math
def range_prod(lo,hi):
    if lo+1 < hi:
        mid = (hi+lo)//2
        return range_prod(lo,mid) * range_prod(mid+1,hi)
    if lo == hi:
        return lo
    return lo*hi

def treefactorial(n):
    if n < 2:
        return 1
    return range_prod(1,n)


def fact(n):
    f = 1
    while n:
        f=f*n
        n-=1
    return f

table = [0.03333333333333333,0.03333333333333333,0.03333333333333333,0.03333333333333333,0.03333333333333333,0.04814814814814814,0.16666666666666666,0.04814814814814814,0.04074074074074074,0.04074074074074074,0.04074074074074074,0.03827160493827161,0.09722222222222221,0.1597222222222222,0.03827160493827161,0.06427469135802469, 0.06388888888888887,0.05555555555555554,0.11481481481481481,0.05041666666666666,0.05041666666666666,0.05041666666666666, 0.03309156378600823, 0.09660493827160493,0.09660493827160493,0.03309156378600823,0.04270833333333333,0.04270833333333333,0.024405006858710564,0.024405006858710564,0.040123456790123455,0.02386917009602195,0.015161965592135345,0.015161965592135345,0.025791859567901233,0.013442072473708277,0.025791859567901233,0.013442072473708277,0.013442072473708277,0.025791859567901233,0.009325964982472184,0.012895929783950617,0.009325964982472184,0.012895929783950617,0.004966801935680536,0.0006076388888888889,0.0006076388888888889,0.0010641043349591016, 0.0010641043349591016,0.0008998945790783924,0.0008998945790783924,0.00012152777777777777,0.0006749209343087943,0.00031394675925925926,0.0006749209343087943,0.00031394675925925926,0.0006749209343087943,0.00012152777777777777,0.00020929783950617283,0.00020929783950617283,0.00020929783950617283,0.00015928974241731438,0.00015928974241731438,6.076388888888889e-05,0.00015928974241731438,6.076388888888889e-05,2.700617283950617e-05,0.00015928974241731438,7.964487120865719e-05,2.700617283950617e-05,4.050925925925926e-05,7.964487120865719e-05,3.375771604938271e-05,2.250514403292181e-05,2.250514403292181e-05,1.5753600823045267e-05,1.0502400548696845e-05,1.0502400548696845e-05,2.250514403292181e-05,1.0502400548696845e-05]
table2 = [0.16666666666666666, 0.16666666666666666, 0.16666666666666666, 0.25,0.25,0.5, 0.5]
table3 = [0.5,0.25,0.1388888888888889,0.1267361111111111,0.1267361111111111,0.16666666666666666,0.07638888888888888,0.1267361111111111,0.041666666666666664,0.06275720164609053,0.06275720164609053,0.06275720164609053,0.041666666666666664,0.06336805555555555,0.044753086419753084,0.011188271604938271,0.011188271604938271,0.011188271604938271,0.011188271604938271,0.021122685185185185,0.021122685185185185,0.021122685185185185]
table4 = [0.041666666666666664,0.3333333333333333,0.3333333333333333,0.2152777777777778,0.18229166666666669,0.18229166666666669,0.15856481481481483,0.11959876543209878,0.11959876543209878,0.07638888888888888,0.07638888888888888,0.05979938271604939,0.05979938271604939,0.041666666666666664]
ent =0
somme = 0
for item in table4:
    ent += -(float(item) * math.log(float(item), 2))
    somme += item
mixnb = 1
ListCascades = {}
for n in range(1, 6+1):
    cascade = []
    for m in range(3):
        varCorrupt = False
        mix = mixnb
        T = m
        mixnb += 1
        cascade.append(mix)
    ListCascades[n] = cascade
g_list = []
group1 = []
group1.append(ListCascades[1])
group1.append(ListCascades[2])
group1.append(ListCascades[3])
g_list.append(group1)

group2 = []
group2.append(ListCascades[1])
group2.append(ListCascades[4])
group2.append(ListCascades[5])
g_list.append(group2)

group3 = []
group3.append(ListCascades[2])
group3.append(ListCascades[4])
group3.append(ListCascades[6])
g_list.append(group3)

group4 = []
group4.append(ListCascades[3])
group4.append(ListCascades[5])
group4.append(ListCascades[6])
g_list.append(group4)

print(g_list)
table = [0.17750506311729866, 0.05270337264361537, 0.10442892447794458, 0.04187700000904571, 0]
s= sum(table)
print(s)