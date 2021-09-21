import json
import pickle
from random import choice
import simpy
import Client
import Mix
from Network import Network
import pandas as pd
import numpy as np
from Relay import Attacker
from util import XRD
from Log import Log
import _pickle as pickle
import dill
import pickle

import random
import uuid
from util import XRD_New
from util import Capacity

import math
DEFAULT_TOPOLOGY = 'stratified'
logDir = 'Logs/'
dummyDropped = []
MsgsDropped = []
dummyID = []
class Simulation(object):

    def __init__(self, rate_client, topology, fully_connected, mix_type, printing,n_clients, flushPercent, logging, flushtime,
                 n_layers, mu, capacity, bandwidth, ClientDummy,LinkDummies, RateDummies,
                 n_mixes_per_layer, corrupt,UniformCorruption,probabilityMixes, simDuration,nbr_cascacdes, Network_template,
                 routing):
        self.Log = Log()
        self.logs = []
        self.logging=logging
        self.printing= printing
        self.topology = topology
        self.fully_connected = fully_connected
        self.LinkDummies = LinkDummies
        self.n_cascades=nbr_cascacdes
        self.ClientDummy = ClientDummy
        self.RateDummies = RateDummies
        self.capacity = capacity
        self.flushPercent = flushPercent
        self.n_clients = n_clients
        self.clientsSet = set()
        self.rate_client = rate_client  # average delay between messages being sent from client
        self.flushthreshold = bandwidth
        self.mu = mu  # average delay at poisson mixes
        self.n_layers = n_layers
        self.n_mixes_per_layer = n_mixes_per_layer
        self.corrupt = corrupt
        self.probabilityMixes = probabilityMixes
        self.UniformCorruption = UniformCorruption
        self.mix_type = mix_type
        self.routing = routing
        self.env = simpy.Environment()
        self.SimDuration = simDuration
        self.flushtime = flushtime
        self.numberTargets =0
        self.MsgsDropped = MsgsDropped
        self.dummyDropped = dummyDropped
        self.dummyID = dummyID
        time_stable = ((1/self.rate_client)/self.n_layers)*self.mu+2
        if self.mix_type == 'poisson':
            self.numberTargets = int(((self.SimDuration-time_stable)*0.5)/2)
            print("Number of targets", self.numberTargets)
        else:
            self.numberTargets = int((self.SimDuration - self.flushtime-1)/2)
        self.network = Network(self.mix_type, self.n_layers, self.n_mixes_per_layer,self.corrupt,self.UniformCorruption, self, self.capacity, self.flushthreshold,
                                        self.flushPercent, self.topology,fully_connected, self.flushtime,self.probabilityMixes, self.n_cascades, self.LinkDummies, self.RateDummies,
                                        Network_template, self.numberTargets)

        self.setupClients(self.probabilityMixes, self.numberTargets, self.ClientDummy, self.Log)
        # self.stableMix = [False for i in range(self.n_mixes_per_layer*self.n_layers)]  # only start attack after mixes are stable
        self.stableChains = [False for i in range(1,1+6)]  # only start attack after chains are stable
        self.stableMixL1 = [False for i in range(self.n_mixes_per_layer)]  # only start attack after mixes are stable
        self.attacker = Attacker(self, self.numberTargets)  # attacker/relay object
        self.endEvent = self.env.event()  # event that triggers the end of the simulation
        self.TargetMessageEnd = False  # if target message has reached the end client
        self.startAttack = False  # if the attacker is allowed to choose a target message
        self.NumberMsgsDropped = 0
        self.numberrounds = []

    def setStableMix(self, index):
        if self.mix_type =='pool':
            yield self.env.timeout(10)
            self.startAttack = True
        elif self.mix_type == 'time':
            yield self.env.timeout(self.flushtime + 5)
            self.startAttack = True
        # self.stableMixL1[index] = True
        if all(self.stableMixL1):
            yield self.env.timeout(2)
            self.startAttack = True
        #else:
        #    yield self.env.timeout(3)
         #   self.stableMix = [True for i in range(self.n_mixes_per_layer * self.n_layers)]  # only start attack after mixes are stable
          #  self.startAttack = True
    def setStableChain(self, position):
        if self.mix_type =='pool':
            yield self.env.timeout(10)
            self.startAttack = True
        self.stableChains[position - 1] = True
        if all(self.stableChains):
            yield self.env.timeout(2)
            self.startAttack = True
        #else:
        #    yield self.env.timeout(3)
         #   self.stableMix = [True for i in range(self.n_mixes_per_layer * self.n_layers)]  # only start attack after mixes are stable
          #  self.startAttack = True

    def setupClients(self, probabilityDistribution, numberTargets, ClientDummy, Log):
        if self.topology == 'stratified':
            for client_no in range(self.n_clients):
                client = Client.Client(self, client_no,self.network.LayerDict , self.rate_client, self.mu,
                                   probabilityDistribution, numberTargets, ClientDummy, Log)
                self.clientsSet.add(client)

            for client in self.clientsSet:
                client.otherClients = self.clientsSet - {client}
        elif self.topology == 'XRD':
            groups_lists = XRD_New(self.network.ListCascades)
            n_group_client = self.n_clients // len(groups_lists)
            for n_client in range(n_group_client):
                client = Client.Client(self, n_client, groups_lists[0], self.rate_client, self.mu,
                                       probabilityDistribution, numberTargets, ClientDummy, Log)
                self.clientsSet.add(client)
            for n_client in range(n_group_client, n_group_client*2):
                client = Client.Client(self, n_client, groups_lists[1], self.rate_client, self.mu,
                                       probabilityDistribution, numberTargets, ClientDummy, Log)
                self.clientsSet.add(client)
            for n_client in range(n_group_client*2, n_group_client*3):
                client = Client.Client(self, n_client, groups_lists[2], self.rate_client, self.mu,
                                       probabilityDistribution, numberTargets, ClientDummy, Log)
                self.clientsSet.add(client)
            for n_client in range(n_group_client*3, self.n_clients):
                client = Client.Client(self, n_client, groups_lists[3], self.rate_client, self.mu,
                                       probabilityDistribution, numberTargets, ClientDummy, Log)
                self.clientsSet.add(client)

            for client in self.clientsSet:
                client.otherClients = self.clientsSet - {client}


    def run(self, time=None):
        # Print statements and results from here
        if self.printing:
            print('\n')
            print('----------Simulation Data----------')
            print('Topology: {}'.format(self.topology))
            print('Routing strategy: {}'.format(self.routing))
            print('Mix type: {}'.format(self.mix_type))
            print('Layers: {}, amount of mixes per layer: {}'.format(self.n_layers, self.n_mixes_per_layer))
            print('Amount of clients: {}, average delay between 2 messages: {}'.format(self.n_clients, self.rate_client))
            l = ''
            index = 0
            if self.topology == 'stratified':
                for layer in self.network.LayerDict:
                    k = 'Layer {}: [ '.format(layer)
                    for mixnb in range(self.n_mixes_per_layer):
                        k += str(self.network.LayerDict[layer][mixnb])
                        k += 'Capacity: '
                        k += str(self.network.LayerDict[layer][mixnb].capacity) + ' )'
                        if self.network.LayerDict[layer][mixnb].corrupt:
                            index += 1
                    l += k + ']'
                    l += '\n'
                print(l)
            elif self.topology == 'cascade':
                k2 = 'Cascade'
                for cascade in self.network.ListCascades:
                    for mixnb in range(3):
                        k2 += str(cascade[mixnb].id)
                        k2 += 'Capacity: '
                    l += k2 + ']'
                    l += '\n'
            print('----------Starting Simulation----------')
        if self.printing:
            print('Topology: {}'.format(self.topology))
        if time is None:
            self.env.run(until=self.endEvent)
        else:
            self.env.run(until=time)

        if self.printing:
            print('----------Simulation Ended---------')
            print('\n')



        #itemsProb[:] = (value for value in itemsProb if value != 0)



        #Data from Clients(senders and receivers)
        df_sent_messages = pd.DataFrame(self.Log.sent_messages)
        df_received_messages = pd.DataFrame(self.Log.received_messages)
        df_dummies_messages = pd.DataFrame(self.Log.dummy_messages)
        df_mix_data = pd.DataFrame(self.Log.mix_data)

        if self.logging:
            df_sent_messages.to_csv(f'{logDir}SentMessages.csv')
            df_received_messages.to_csv(f'{logDir}ReceivedMessages.csv')
            df_dummies_messages.to_csv(f'{logDir}DummyMessages.csv')
            df_mix_data.to_csv(f'{logDir}MixData.csv')
        else:
            pass

        ent = []
        for i in range(0, self.numberTargets):
            ent.append(0.0)
        tableProb = df_received_messages['MessageTarget'].to_numpy(copy=True)
        for j in range(0, self.numberTargets):
            for m in range(len(tableProb)):
                if tableProb[m][j] != 0:
                    ent[j] += - tableProb[m][j] * np.log2(tableProb[m][j])


        dict_entropy = {'Entropy': ent}
        df_entropy = pd.DataFrame(dict_entropy)
        df_entropy.to_csv(f'{logDir}{self.n_layers}Entropy.csv')

        entropy_mean = np.mean(ent)
        try:
            entropy_median = np.median(ent)
            entropy_q25 = np.quantile(ent, .25)
        except:
            entropy_median = 0
            entropy_q25 = 0

        avg_delayLog = 0
        for re, le in zip(self.Log.received_messages["MessageTimeReceived"],self.Log.received_messages["MessageTimeLeft"]) :
            avg_delayLog += (re - le)
        avg_delayLogN = avg_delayLog / len(self.Log.received_messages["MessageTimeReceived"])
        if self.printing:
            print('----------Simulation Stats----------')
            #print('Average Latency: {}'.format(latency))
            print("Number of targets chosen", self.numberTargets)
            print('Number of Real messages generated', len(self.Log.sent_messages["MessageID"]))
            print('Number of Real messages Received', len(self.Log.received_messages["MessageID"]))
            print('Number of Total messages dropped', len(self.MsgsDropped))
            print('Number of Dummy messages dropped', len(self.Log.dummy_messages["DummyID"]))
            print("Average delay per message",avg_delayLogN)

        return ent, entropy_mean, entropy_median, entropy_q25
