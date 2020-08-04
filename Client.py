from util import sample_from_exp_dist
import numpy as np
import random

import simpy
from numpy.random import choice
from Message import Message
import pandas as pd

tableID = []
tableS = []
tableID2 = []
tableS2 = []
tableRT = []
tableC = []
tableR = []
tableD = []
tableT = []
tableM1 = []
var = True


class Client:
    ClientList = ["Client 2", "Client 5", "Client 6", "Client10"]

    def __init__(self, simulation, ide, layer1, layer2, layer3, rate, nbr_msgs):
        global var
        self.ide = ide
        self.env = simulation.env
        self.envC = simpy.Environment()
        self.simulation = simulation
        self.layer1 = layer1
        self.layer2 = layer2
        self.layer3 = layer3
        self.class_ends = self.env.event()
        self.buffer = []
        self.log = []
        self.rateS = rate
        self.nbr_msgs = nbr_msgs
        self.tableID = tableID
        self.tableS = tableS  # sender table
        self.tableID2 = tableID2 
        self.tableS2 = tableS2
        self.tableRT = tableRT
        self.tableC = tableC
        self.tableR = tableR
        self.tableD = tableD
        self.tableT = tableT
        self.tableM1 = tableM1
        self.type = ['Real', 'Dummy']
        self.rateM = 0.1

        for i in range(self.nbr_msgs):
            if i == int(self.nbr_msgs/2) and self.ide == simulation.n_clients //2 and var == True:
                target = 1
                trace = []
                tag = True
                delayC = sample_from_exp_dist(self.rateS)
                delay1 = sample_from_exp_dist(self.rateM)
                delay2 = sample_from_exp_dist(self.rateM)
                delay3 = sample_from_exp_dist(self.rateM)
                delay = [delay1, delay2, delay3]
                elements1 = [self.layer1[0], self.layer1[1], self.layer1[2]]
                elements2 = [self.layer2[0], self.layer2[1], self.layer2[2]]
                weights = [0.1, 0.1, 0.8]
                First_node = random.choice(self.layer1)
                Second_node = random.choice(self.layer2) #np.random.choice(elements2, p=weights)
                Third_node = random.choice(self.layer3)
                if simulation.routing == 'source':
                    tmp_route = [First_node, Second_node, Third_node]
                    Tmp = [tmp_route[0].mix_id, tmp_route[1].mix_id, tmp_route[2].mix_id]
                else:
                    tmp_route = [First_node, None, None]
                    Tmp = [tmp_route[0].mix_id, None, None]

                tableR.append(Tmp)
                t = random.choice(self.type)
                msg = Message(i + 1, t, self, self.ide, random.choice(self.ClientList), delayC, tmp_route, delay,
                              target, tag,
                              trace)

                self.buffer.append(msg)
                tableID.append(msg.id)
                tableC.append(delayC)
                tableD.append(delay)
                tableT.append(t)
                var = False
                print("Client %d Created a target %s of probability %f " % (self.ide, msg.id, target))
                print(Tmp)
            else:
                tag = False
                delayC = sample_from_exp_dist(self.rateS)
                delay1 = sample_from_exp_dist(self.rateM)
                delay2 = sample_from_exp_dist(self.rateM)
                delay3 = sample_from_exp_dist(self.rateM)
                delay = [delay1, delay2, delay3]
                elements1 = [self.layer1[0], self.layer1[1], self.layer1[2]]
                elements2 = [self.layer2[0], self.layer2[1], self.layer2[2]]
                weights = [0.1, 0.1, 0.8]
                First_node = random.choice(self.layer1) #np.random.choice(elements1, p=weights)
                Second_node = random.choice(self.layer2) #np.random.choice(elements2, p=weights)
                Third_node = random.choice(self.layer3)
                if simulation.routing == 'source':
                    tmp_route = [First_node, Second_node, Third_node]
                    Tmp = [tmp_route[0].mix_id, tmp_route[1].mix_id, tmp_route[2].mix_id]
                else:
                    tmp_route = [First_node, None, None]
                    Tmp = [tmp_route[0].mix_id, None, None]

                tableR.append(Tmp)
                t = random.choice(self.type)
                msg = Message(i + 1, t, self, self.ide, random.choice(self.ClientList), delayC, tmp_route, delay, 0,
                              tag,
                              None)
                self.buffer.append(msg)
                tableID.append(msg.id)
                tableC.append(delayC)
                tableD.append(delay)
                tableT.append(t)

    def send_msg(self, env):
        for msg in self.buffer:
            event = simpy.events.Timeout(env, delay=msg.delayC)
            yield event
            self.tableID2.append(msg.id)
            now = env.now
            self.tableRT.append(now)
            tmp1 = [msg.id, now, False]
            self.log.append(tmp1)
            #self.waitAck(msg, now)
            #p22 = simpy.events.Process(self.env, self.waitAck(msg, now))
            if self.simulation.mix_type == 'time':
                msg.route[0].add_msg_in_pool(msg, now)
                p = simpy.events.Process(env, msg.route[0].add_msg_in_pool(msg, now))
            else:
                msg.route[0].add_msg_in_pool(msg, env)
                p = simpy.events.Process(env, msg.route[0].add_msg_in_pool(msg, env))

    def receiveAck(self, msg):
        for obj in self.log:
            if obj[0] == msg.id:
                obj[2] = True

    def waitAck(self, msg, now):
        event66 = simpy.events.Timeout(self.env, delay=now + 50)
        yield event66
        for obj in self.log:
            if obj[0] == msg.id:
                if not obj[2]:
                    print("Message %s was sent at %f and now is %f Didnt go through" % (msg.id, now, self.env.now))
        """    def printForEncC(self,msg, now, envv):
        yield self.envC.timeout(now + 50)
        for obj in self.log:
            if obj[0] == msg.id:
                if obj[2] == False:
                    print("CCMessage %s was sent at %f and now is %f Didnt go through" % (msg.id, now, self.envC.now))

"""

