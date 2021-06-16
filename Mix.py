from Client import Client
from numpy.random import exponential
from Message import Message
from random import choice, sample
import numpy as np
event = []
msgID = []
mixID = []
time = []
msgType = []

effectivePoolsize = []  # effective poolsize of mixes
mixID2 = []
time2 = []
probArray = []  # probability the target message resides in the mix


class Mix:
    def __init__(self, id, simulation, position, capacity, numberTargets, corrupt):
        self.event = event  # logging
        self.time = time
        self.time2 = time2
        # logging
        self.effectivePoolsize = effectivePoolsize
        self.numberTargets = numberTargets
        self.id = id
        self.env = simulation.env
        self.simulation = simulation
        self.layer = position  # 1, 2, 3, ... this has no meaning in a freeroute simulation!
        self.capacity = capacity
        self.corrupt = corrupt  # corrupt mix or not
        self.Pmix = []# probability this mix contains the target message

        for i in range(0, self.numberTargets):
            self.Pmix.append(float(0.0))
        self.sender_estimate =[0.0,0.0, 0.0]
        self.NumberOfrealMessages=0
        self.NumberOfDummies = 0

    def createDummiesRate(self, dummyNb):
        layerDict = self.simulation.network.LayerDict
        route = [None]
        delaylist = [0]
        for layer in range(1, self.simulation.n_layers + 1):
            if self.layer > layer:
                route.append(None)
                delaylist.append(0)
            elif self.layer == layer:
                route.append(self)
                delaylist.append(exponential(self.simulation.mu))
            else:
                route.append(choice(layerDict[layer]))
                delaylist.append(exponential(self.simulation.mu))
        delaylist += [0]
        newstop = sample(self.simulation.clientsSet, k=1)[0]
        route += [newstop]
        tablePR = []
        target = []
        for j in range(0, self.numberTargets):
            target.append(float(0.0))
        sender_estimate = [0.0, 0.0, 1.0]
        newDummy = Message(dummyNb, 'Dummy', self, route, delaylist, target, False, tablePR, sender_estimate)

        newDummy.nextStopIndex = self.layer + 1
        newDummy.id = f'd_{self.id}_{dummyNb}'
        self.simulation.dummyID.append(newDummy.id)
        return newDummy

    def __str__(self):
        return f'( id: {self.id}, corrupt: {self.corrupt} )'

    def __repr__(self):
        return self.__str__()


