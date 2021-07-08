from random import choice, sample
from Message import Message
from numpy.random import exponential
import numpy as np
from Log import Log
import random
from array import array

ProbabilitiesEntropy = []
delayTable = []  # total latency of a message
tableAverageDelay = []  # IDs of message received
tableType = []  # IDs of message received
targetProbability = 0  # Probability of taget message when it arrives at its destination

class Client:
    def __init__(self, simulation, id, topology, rateC, mu, probabilityDistribution, numberTargets, ClientDummy, Log):
        self.id = id
        self.env = simulation.env
        self.simulation = simulation  # simulation object
        self.layerDict = topology
        self.class_ends = self.env.event()
        self.mu = mu  # Avg delay: for delays at the poisson mixes
        self.probabilityDistribution = probabilityDistribution
        self.otherClients = set()
        self.messageIDs = 1
        self.delay = delayTable

        self.tableAverageDelay = tableAverageDelay
        self.rateC = rateC
        self.allMixes = []
        self.numbertargets=numberTargets
        self.ClientDummy = ClientDummy
        self.log = Log
        if self.simulation.topology == 'stratified':
            for layer in range(1, len(self.layerDict) + 1):
                self.allMixes += self.layerDict[layer]
        elif self.simulation.topology == 'XRD':
            self.set_chains = self.layerDict
        self.env.process(self.sendMessages('Real', self.rateC))
        if self.ClientDummy is not None:
            self.env.process(self.sendMessages('ClientDummy', self.ClientDummy))

    def createMessage(self, Msgtype, rate):
        np.random.seed()
        delayC = exponential(rate)
        tmp_route = [self]
        Tmp = [self.id]
        delay = [delayC]
        tablePr= []
        target = []

        for i in range(0, self.numbertargets):
            target.append(float(0.0))
        for layer in range(1, self.simulation.n_layers+1):
            delay_per_mix = exponential(self.mu)
            delay.append(delay_per_mix)
            if self.simulation.routing == 'source' and self.simulation.topology == 'stratified'\
                    or (self.simulation.routing == 'hopbyhop' and self.simulation.topology == 'stratified' and layer == 1):
                if self.simulation.n_layers ==1 and self.simulation.n_mixes_per_layer == 1:
                    node = self.layerDict[1][0]
                    tmp_route.append(node)
                    Tmp.append(node.id)
                else:
                    node = np.random.choice(self.layerDict[layer], p=self.probabilityDistribution[layer - 1])
                    tmp_route.append(node)
                    Tmp.append(node.id)

            elif self.simulation.routing == 'source' and self.simulation.topology == 'freeroute'\
                    or (self.simulation.routing == 'hopbyhop' and self.simulation.topology == 'freeroute' and layer == 1):

                node = choice(self.allMixes)
                while node in tmp_route:
                    node = choice(self.allMixes)
                tmp_route.append(node)
                Tmp.append(node.id)

            elif self.simulation.routing == 'hopbyhop' and layer != 1:
                tmp_route.append(None)
                Tmp.append(None)
            elif self.simulation.routing == 'source' and self.simulation.topology == 'XRD':
                chain = random.choice(self.set_chains)
                for node in chain:
                    tmp_route.append(node)
                    Tmp.append((node.id))
        delay += [0]
        receiver = sample(self.otherClients, k=1)[0]
        tmp_route += [receiver]
        Tmp += [receiver.id]
        if self.simulation.startAttack:
            sampling = True
            if self.id == 1:
                sender_estimate = [1.0,0.0,0.0]
            elif self.id == 2 :
                sender_estimate = [0.0,1.0,0.0]
            else:
                sender_estimate = [0.0,0.0,1.0]
        else:
            sender_estimate = [0.0, 0.0, 1.0]
            sampling = False

        msg = Message(self.messageIDs, Msgtype, self, tmp_route, delay, target,False, tablePr, sender_estimate)
        msg.sampling =sampling
        if self.messageIDs == 1 and self.id ==1:
            for i in range(len(self.probabilityDistribution)):
                if self.simulation.printing:
                    print("Weights Layer %d %s"%(i, self.probabilityDistribution))
                else:
                    pass
        self.messageIDs += 1
        return msg, delayC



    def receive_msg(self, msg):
        # if msg.type != 'Malicious Dummy':
            if msg.sender.id ==1 or msg.sender.id == 2:
                self.log.MessagesLD(msg)
            self.log.ReceivedMessage(msg)
            if self.simulation.mix_type == 'poisson':
                self.delay.append(self.env.now - msg.timeLeft)
            elif self.simulation.mix_type == 'time':
                self.delay.append(self.env.now - msg.timeLeft)
            else:
                self.delay.append(self.env.now - msg.timeLeft)
            d = self.env.now - msg.timeLeft


            self.tableAverageDelay.append(d)
            if msg.tag:
                global targetProbability
                self.simulation.TargetMessageEnd = True
                targetProbability = msg.target
                if self.simulation.printing:
                    print(f'Target message arrived at destination Client at time {self.env.now}')
            if msg.type == 'Real' or msg.type == 'ClientDummy':
                msg.route[0].receiveAck(msg)

    def sendMessages(self, msgtype, rate):
        while True:
            msg, delay = self.createMessage(msgtype, rate)
            yield self.env.timeout(delay)
            msg.timeLeft = self.env.now
            self.log.SentMessage(msg)
            self.env.process(self.simulation.attacker.relay(msg, msg.route[1], self))

    def receiveAck(self, msg):  # Message received
        pass

    def __str__(self):
        return 'Client id: {}'.format(self.id)

    def __repr__(self):
        return self.__str__()