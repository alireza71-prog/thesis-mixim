from random import sample, choice
from Client import Client
from Mix import Mix
from numpy.random import exponential
from Message import Message
import numpy as np
import random

global idDummies


class PoissonMix(Mix):
    def __init__(self, mix_id, simulation, position, capacity,LinkDummies,RateDummies, numberTargets, corrupt, prob):
        super().__init__(mix_id, simulation, position, capacity, numberTargets, corrupt)
        self.pool = []  # Pool
        self.neighbors = set()
        self.index = 0
        self.LinkDummies = LinkDummies
        self.RateDummies = RateDummies
        self.prob = prob
        self.pool_dummies = []
        if self.RateDummies is not None and not self.corrupt and self.layer != self.simulation.n_layers:
            self.env.process(self.sendDummiesRate())

    def receive_msg(self, msg):
        if not self.simulation.startAttack:  # if a mix reaches a poolsize of 5 percent higher than the average,
            # the GPA can monitor the network and choose a target message
            clients = self.simulation.n_clients
            lambdaClient = self.simulation.rate_client
            n = self.simulation.n_mixes_per_layer
            var1 = len(self.pool) >= ((clients * lambdaClient / n) * self.simulation.mu) * self.prob
            if self.simulation.topology == 'stratified':
                  # average poolsize
                if var1:
                    self.env.process(self.simulation.setStableMix(self.id - 1))
                if all(self.simulation.stableMixL1):
                    for i in range(len(self.simulation.stableMix)):
                        self.simulation.setStableMix(i)
            elif self.simulation.topology == 'XRD':
                if var1:
                    self.env.process(self.simulation.setStableChain(self.n_chain))
                if all(self.simulation.stableChains):
                    for i in range(len(self.simulation.stableChains)):
                        self.simulation.setStableChain(i)

        if len(self.pool) < self.capacity:

            for i in range(0, self.numberTargets):
                self.Pmix[i] += msg.target[i]
            self.sender_estimate = [x+y for x,y in zip(self.sender_estimate, msg.sender_estimate)]
            if msg.tag and self.simulation.printing:
                print(f'Target message arrived at mix {self.id} at time {self.env.now} and Number of real messages{len(self.pool)} and number of dummies{len(self.pool_dummies)}')
            msg.nextStopIndex += 1
            if msg.route[msg.nextStopIndex] == None:
                msg.route[msg.nextStopIndex] = random.choice(self.neighbors)
            if msg.type == 'Real':
                self.pool.append(msg)
                self.env.process(self.send_msg(msg))
            elif msg.type == 'Dummy':
                if self.LinkDummies == True:
                    self.DropDummies(msg)
                elif self.LinkDummies ==False:
                    if self.layer == self.simulation.n_layers:
                        self.DropDummies(msg)
                    elif self.layer != self.simulation.n_layers:
                        self.pool.append(msg)
                        self.env.process(self.send_msg(msg))
        else:
            self.DropFullCapacity(msg)

    def DropFullCapacity(self, msg):
        self.simulation.MsgsDropped.append(msg.id)

    def DropDummies(self, msg):
        if self.layer == 3:
            self.simulation.Log.Dummies_Dropped_end_link( msg, self.id)
        #self.pool.remove(msg)

    def uncertainMessage(self, msg):
        # returns True if this messages adds entropy to the attacker

        if msg.type == 'Malicious Dummy':
            return False
        return True

    def send_msg(self, msg):
        yield self.env.timeout(msg.delay[self.layer])
        if not isinstance(msg.route[msg.nextStopIndex], Client) and msg.route[
            msg.nextStopIndex] is None:  # not the last mix
            msg.route[msg.nextStopIndex] = sample(self.neighbors, k=1)[0]

        effectivePoolsize = len(self.pool)
        self.computeProba(msg, effectivePoolsize)
        nextStop = msg.route[msg.nextStopIndex]
        self.pool.remove(msg)

        self.env.process(self.simulation.attacker.relay(msg, nextStop, self))


    def computeProba(self, msg, poolsize):
        if not self.corrupt:
            if self.uncertainMessage(msg):  # Returns False if the message is a Malicious dummy sent by the attacker and the mix is corrupted
                for j in range(0, self.numberTargets):
                    msg.target[j] = self.Pmix[j] / poolsize
                    msg.tablePr.append(msg.target[j])
                    self.Pmix[j] = self.Pmix[j] - msg.target[j]
                msg.sender_estimate = [x / poolsize for x in self.sender_estimate]
                self.sender_estimate = [x - y for x, y in zip(self.sender_estimate, msg.sender_estimate)]

    def sendDummiesRate(self):
        dummy_id = 1
        while True:
            newMessage = self.createDummiesRate(dummy_id)
            newMessage.creator = self.id
            self.pool.append(newMessage)
            yield self.env.timeout(exponential(self.RateDummies))
            dummy_id += 1
            self.env.process(self.send_msg(newMessage))