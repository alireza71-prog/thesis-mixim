from PoissonMix import PoissonMix
from Pool import Pool
from TimedMix import TimedMix
from util import OptimizedPositions
from util import RandomPosition
import numpy as np
from random import choice
import random

class Network:
    MixesAll = []
    LayerDict = {}  # 1:[list of mixes in layer 1], 2:[list of mixes in layer 2], ...

    def __init__(self, mix_type, num_layers, nbr_mixes_layers,corrupt,UniformCorruption, simulation, capacity, flushThreshold,
                 flushPercent, topology, flushtime, probabilityDistribution, n_cascades,LinkDummies, RateDummies, Network_template, numberTargets):
        self.simulation = simulation
        self.num_layers = num_layers
        self.mix_type = mix_type
        self.mixesPerLayer = nbr_mixes_layers
        self.corrupt = corrupt
        self.UniformCorruption= UniformCorruption
        self.env = simulation.env
        self.capacity = capacity
        self.bandwidth = flushThreshold
        self.flushPercent = flushPercent
        self.topology = topology
        self.flushtime = flushtime
        self.n_cascades = n_cascades
        self.LinkDummies = LinkDummies
        self.RateDummies  = RateDummies
        self.probabilityDistribution = probabilityDistribution
        self.Network_template = Network_template
        self.numberTargets = numberTargets
        self.ListCascades = {}
        self.n_cascades = 6
        self.createNetwork()

    def createNetwork(self):
        mixnb = 1
        self.MixesAll = set()
        if self.topology == 'stratified':
            Nbr_Corruption=0
            for layer in range(1, self.num_layers + 1):
                c = 0
                self.LayerDict[layer] = []
                for _ in range(self.mixesPerLayer):
                    if self.UniformCorruption:
                        if c < self.corrupt/self.simulation.n_layers:
                            varCorrupt = True
                            c += 1
                        else:
                            varCorrupt = False
                    else:
                        if Nbr_Corruption < self.corrupt:
                            varCorrupt = random.choice([True, False])
                            if varCorrupt:
                                Nbr_Corruption+=1
                        else:
                            varCorrupt = False
                    mix = self.get_mixnode(self.mix_type, mixnb, layer, self.numberTargets, varCorrupt,
                                           self.probabilityDistribution[layer - 1][_])
                    self.MixesAll.add(mix)
                    self.LayerDict[layer] += [mix]
                    mixnb += 1
            for mix in self.MixesAll:
                if mix.layer + 1 in self.LayerDict:  # last mix doesn't need neighbors
                    mix.neighbors = self.LayerDict[mix.layer + 1]
                if mix.layer == self.simulation.n_layers:
                    mix.neighbors = self.LayerDict[1]
        elif self.topology == 'XRD':
            mixnb = 1
            for n in range(1,1+self.n_cascades):
                cascade = []
                for m in range(self.num_layers):
                    varCorrupt = False
                    mix = self.get_mixnode(self.mix_type, mixnb, m+1, self.numberTargets, varCorrupt,
                                       1/self.n_cascades)
                    mix.n_chain = n
                    self.MixesAll.add(mix)
                    mixnb += 1
                    cascade.append(mix)
                self.ListCascades[n] = cascade
            for n, list in self.ListCascades.items():
                print('Chain number',n, ':', list)

    def get_mixnode(self, mix_type, id, position, numberTargets, corrupt, probability):
        capacity = 1000
        if self.topology == 'stratified':
            arr = self.capacity
            capacity = arr[position - 1][id - 1 - (position - 1) * self.simulation.n_mixes_per_layer]
        elif self.topology == 'XRD':
            capacity = 10000
        if mix_type == 'poisson':
            return PoissonMix(id, self.simulation, position, capacity,self.LinkDummies, self.RateDummies, numberTargets, corrupt, probability)
        elif mix_type == 'pool':
            return Pool(id, self.simulation,  position,capacity, self.bandwidth, self.flushPercent, numberTargets, corrupt, probability)
        elif mix_type == 'time':
            return TimedMix(id, self.simulation,  position,capacity,self.flushtime,numberTargets,corrupt, probability)

    def odd(self, number):
        return number % 2 == 1

