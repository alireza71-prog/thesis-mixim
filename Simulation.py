import json
import random

import simpy
from Client import Client
from Network import Network
import pandas as pd
import numpy as np
import psutil

DEFAULT_NUM_OF_STEPS = 100000
DEFAULT_NUM_OF_MIXES_PER_LAYER = 3
DEFAULT_NUM_OF_LAYERS = 3
DEFAULT_MIXTYPE = 'poisson'
DEFAULT_ROUTING = 'SOURCE'


class Simulation(object):

    def __init__(self, n_clients, n_msgs, rate_client,
                 n_layers=DEFAULT_NUM_OF_LAYERS,
                 n_mixes_per_layer=DEFAULT_NUM_OF_MIXES_PER_LAYER,
                 n_steps=DEFAULT_NUM_OF_STEPS, mix_type=DEFAULT_MIXTYPE, routing=DEFAULT_ROUTING):
        self.logs = []
        self.n_clients = n_clients
        self.listClients = []
        self.n_msgs = n_msgs
        self.rate_client = rate_client
        self.n_layers = n_layers
        self.n_mixes_per_layer = n_mixes_per_layer
        self.n_steps = n_steps
        self.mix_type = mix_type
        self.routing = routing
        self.env = simpy.Environment()

    def run(self):
        network = Network(self.mix_type, self.n_layers, self.n_mixes_per_layer, self)
        for client_no in range(self.n_clients):
            client = Client(self, client_no, network.Firstlayer, network.SecondLayer, network.ThirdLayer,
                            self.rate_client, self.n_msgs)
            self.listClients.append(client)
            p = simpy.events.Process(self.env, client.send_msg(self.env))

        self.env.run(until=self.n_steps)
        """for lm in range(len(self.listClients)):
            self.listClients[lm].envC.run(until=self.n_steps)
"""
        if self.mix_type == 'time':
            for i in range(len(network.MixesAll)):
                network.MixesAll[i].env2.run(until=self.n_steps)
        else:
            pass
        # self.dump_log()


        dict1 = {'Message ID': client.tableID, 'Type': client.tableT, 'Creation': client.tableC, 'Route': client.tableR,
                 'Delay': client.tableD}
        df = pd.DataFrame(dict1)
        df.to_csv('FileMessagesClients.csv')
        print(df)

        dict2 = {'Data from Mix 1': network.MixesAll[0].tableL1}
        df2 = pd.DataFrame(dict2)
        df2.to_csv('FileMessagesLeftM1.csv')
        print(df2)

        dict3 = {'Data from Mix 2': network.MixesAll[0].tableL2}
        df3 = pd.DataFrame(dict3)
        df3.to_csv('FileMessagesLeftM2.csv')
        print(df3)
        dict4 = {'Data from Mix 3': network.MixesAll[0].tableL3}
        df4 = pd.DataFrame(dict4)
        df4.to_csv('FileMessagesLeftM3.csv')
        print(df4)
        print("******************Tables for LatencY*********************")
        dict5 = {'Message ID': client.tableID2, 'Time Left Client': client.tableRT}
        df5 = pd.DataFrame(dict5)
        df5.to_csv('FileMessagesLeftClient.csv')
        print(df5)
        MLID = []
        TableTime = []
        tableProb = []
        tablep = []
        for i in range(len(network.MixesAll[0].tableL3)):
            MLID.append(network.MixesAll[0].tableL3[i][0])
            TableTime.append(network.MixesAll[0].tableL3[i][1])
            tableProb.append(network.MixesAll[0].tableL3[i][3])
            if network.MixesAll[0].tableL3[i][4] != 1:
                tablep.append(network.MixesAll[0].tableL3[i][3])
            if network.MixesAll[0].tableL3[i][4] == 1:
                print("This is target", network.MixesAll[0].tableL3[i][3])
                epsilontarget= network.MixesAll[0].tableL3[i][3]

        dict40 = {'Message ID': MLID, 'Time Left Mix 3': TableTime,'Prob': tableProb }
        df40 = pd.DataFrame(dict40)
        print(df40)
        merged_inner = pd.merge(left=df5, right=df40, left_on=['Message ID'],
                                right_on=['Message ID'])
        sum_column = merged_inner["Time Left Mix 3"] - merged_inner["Time Left Client"]
        print("LATENCY FOR THIS SIMULATION", sum_column.mean())
        merged_inner["Latency per message"] = sum_column
        print(merged_inner)

        print("Number of messages left in each node:")
        print("Mix 0", len(network.MixesAll[0].pool))
        print("Mix 1", len(network.MixesAll[1].pool))
        print("Mix 2", len(network.MixesAll[2].pool))
        print("Mix 3", len(network.MixesAll[3].pool))
        print("Mix 4", len(network.MixesAll[4].pool))
        print("Mix 5", len(network.MixesAll[5].pool))
        print("Mix 6", len(network.MixesAll[6].pool))
        print("Mix 7", len(network.MixesAll[7].pool))
        print("Mix 8", len(network.MixesAll[8].pool))
        nbr = 0
        for obj1 in network.MixesAll:
            if obj1.corrupt:
                nbr+=1
            else:
                pass
        per = (nbr*100)/len(network.MixesAll)
        print("Percentage of corrupted MIixes %.2f " % per)
        ent = 0
        for m in range(len(tableProb)):
            if tableProb[m] == 0:
                pass
            else:
                ent = ent - tableProb[m] * np.log2(tableProb[m])
        print("3 layers")
        print("Entropy", ent)
        tablep.sort()
        epsiolonclosest = tablep[-1]
        while True:
            epsilonrandom = random.choice(tableProb)
            if epsilonrandom != 0:
                break
        ratio = epsilontarget/ epsilonrandom

        indis = np.log2(epsilontarget/epsilonrandom)
        indis2 = np.log2(epsilontarget/epsiolonclosest)
        print("Indistinguishibility", indis)
        print("Indistinguishibility Closest", indis2)
        print("Ratio", ratio)



        """for client_no in self.listClients:
            for obj in client_no.log:
                if obj[2] == False:
                    print("Message Received No Ack")
"""
    def dump_log(self):
        with open("sim_results.json", "w") as f:
            f.write(json.dumps({'results': self.logs}))

    def log_event(self, event_type, event_time, src_id, dst_node=None, msg_id=None, msg_type=None):
        self.logs.append([event_type, event_time, src_id, dst_node, msg_id, msg_type])
