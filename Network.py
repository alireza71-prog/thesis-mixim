import random

from PoissonMix import PoissonMix
from Pool import Pool
from TimedMix import TimedMix
import numpy as np
import weakref


def get_mixnode(mix_type):
    if mix_type == 'poisson':
        return PoissonMix
    elif mix_type == 'pool':
        return Pool
    elif mix_type == 'time':
        return TimedMix
    else:
        raise ValueError(f'Unkown mix_type: {mix_type}')


class Network(object):
    MixesAll = []
    nbr_mixes_network: int = 9
    position = ['Entry', 'Middle', 'Exit']
    topology = {}
    Firstlayer = []
    SecondLayer = []
    ThirdLayer = []
    layers0 = []
    layers1 = []
    layers2 = []

    def __init__(self, mix_type, num_layers, nbr_mixes_layers, simulation):
        self.simulation = simulation
        self.num_layers = num_layers
        self.nbr_mixes_layers = nbr_mixes_layers
        self.env = simulation.env
        v = [True, False]
        nbr = int(random.uniform(0,2))
        nbr2 = random.uniform(3,5)
        for i in range(self.nbr_mixes_network // 3):
            corr = np.random.choice(v, p=[0.3, 0.7])
            bandwidth = 50
            if i == 0 or i == 1:
                m = get_mixnode(mix_type)(i, simulation, bandwidth, 'Entry', False)
            else:
                m = get_mixnode(mix_type)(i, simulation, bandwidth, 'Entry', False)
            self.MixesAll.append(m)
        for j in range(self.nbr_mixes_network // 3, (self.nbr_mixes_network // 3) * 2):
            corr = np.random.choice(v, p=[0.3, 0.7])
            bandwidth = 50 # random.randint(10, 20)
            if j == 3 or j == 4 :
                m = get_mixnode(mix_type)(j, simulation, bandwidth, 'Middle', False)
            else:
                m = get_mixnode(mix_type)(j, simulation, bandwidth, 'Middle', False)

            self.MixesAll.append(m)
        for k in range(((self.nbr_mixes_network // 3) * 2), ((self.nbr_mixes_network // 3) * 3)):
            corr = np.random.choice(v, p=[0.3, 0.7])
            bandwidth = 50  # random.randint(10, 20)
            if k == 6 or k == 7:
                m = get_mixnode(mix_type)(k, simulation, bandwidth, 'Exit', False)
            else:
                m = get_mixnode(mix_type)(k, simulation, bandwidth, 'Exit', False)

            self.MixesAll.append(m)

        for obj in self.MixesAll:
            if obj.position == 'Entry':
                self.Firstlayer.append(obj)
                tmp = [obj.mix_id, obj.bandwidth, obj.corrupt]
                self.layers0.append(tmp)
            elif obj.position == 'Middle':
                self.SecondLayer.append(obj)
                tmp = [obj.mix_id, obj.bandwidth, obj.corrupt]
                self.layers1.append(tmp)
            else:
                self.ThirdLayer.append(obj)
                tmp = [obj.mix_id, obj.bandwidth, obj.corrupt]
                self.layers2.append(tmp)
        if simulation.routing == 'hopbyhop' or simulation.routing == 'source':
            for obj in self.MixesAll:
                if obj.position == 'Entry':
                    obj.neighbors = self.SecondLayer
                elif obj.position == 'Middle':
                    obj.neighbors = self.ThirdLayer
                else:
                    pass
        else:
            pass

        layers = [self.Firstlayer, self.SecondLayer, self.ThirdLayer]
        print("Layer 0", self.layers0)
        print("Layer 1", self.layers1)
        print("Layer 2", self.layers2)
        for obj2 in self.MixesAll:
            if obj2.position == 'Entry':
                self.topology[obj2] = layers[1]
            elif obj2.position == 'Middle':
                self.topology[obj2] = layers[2]
            else:
                pass
