import simpy
from numpy import random
from Message import Message
import numpy as np

DEFAULT_SENDING_RATE = 0.1

StartComputing = False


class Pool:
    tableL1 = []
    tableL2 = []
    tableL3 = []
    tableID1 = []
    tableID2 = []
    tableID3 = []
    tableS1 = []
    tableS2 = []
    tableS3 = []
    tableM1 = []
    tableM2 = []
    tableM3 = []
    # For dropped Messages
    tableMsg = []
    tableTime = []
    tableMix = []

    tableP1 = []
    tableP2 = []
    tableP3 = []

    def __init__(self, mix_id, simulation, bandwidth, position, corrupt=False):
        self.mix_id = mix_id
        self.pool = []
        self.poolD = []
        self.log = []
        self.ctr = 0
        self.simulation = simulation
        self.env = simulation.env
        self.entropy = 0
        self.neighbors = []
        self.bandwidth = bandwidth
        self.position = position
        self.corrupt = corrupt
        self.round = 0
        self.VectorP = [0]
        self.gotthetarget = False
        self.startcomputation = False
        self.entropy = 0
        self.prob = 0
        self.roundCame = 0
        self.entropy = 0
        for i in range(int(0.3 * self.bandwidth)):
            trace = []
            delayC = 0
            delay = [0, 18.52, 3.74]
            if self.position == 'Entry':
                tmp_route = [self, None, None]
            elif self.position == 'Middle':
                tmp_route = [None, self, None]
            else:
                tmp_route = [None, None, self]

            t = 'dummy'
            msg = Message(i * 666, t, self, self.mix_id, 'NoOne', delayC, tmp_route, delay, 0, False, trace)
            self.pool.append(msg)

    def add_msg_in_pool(self, msg, env):
        event2 = simpy.events.Timeout(env, delay=1)
        yield event2
        self.ctr += 1
        self.pool.append(msg)
        now = env.now
        tpr = [msg, now]
        self.log.append(tpr)
        self.prob = self.prob + msg.target
        if msg.target == 1:
            self.roundCame = self.round + 1
        if len(self.pool) == self.bandwidth or len(self.pool) > self.bandwidth:
            self.ctr = 0
            self.round += 1
            self.send_msg(env)
            self.prob = self.prob - self.prob * 0.7

        else:
            pass

    def send_msg(self, env):
        if self.position == 'Entry':
            k = 0
            i = 0
            try:
                while k < int(0.7 * self.bandwidth):
                    i = random.randint(0, len(self.pool))
                    if self.pool[i].route[1] is None:
                        self.pool[i].route[1] = random.choice(self.neighbors)
                    else:
                        pass
                    self.computeProba(self.pool[i])
                    if self.pool[i].tag is True:
                        t = [self.roundCame, self.round, self.pool[i].target]
                        self.pool[i].trace.append(t)
                        print(self.pool[i].trace)
                    self.pool[i].route[1].add_msg_in_pool(self.pool[i], env)
                    p = simpy.events.Process(env, self.pool[i].route[1].add_msg_in_pool(self.pool[i], env))
                    tr = [self.pool[i].id, env.now, self.pool[i].route[0].mix_id]
                    self.tableL1.append(tr)
                    self.delete_msg(self.pool[i])
                    k += 1
            except:
                RuntimeError

        elif self.position == 'Middle':
            k = 0
            i = 0
            try:
                while k < int(0.7 * self.bandwidth):
                    i = random.randint(0, len(self.pool))
                    if self.pool[i].route[2] is None:
                        self.pool[i].route[2] = random.choice(self.neighbors)
                    else:
                        pass
                    self.computeProba(self.pool[i])
                    if self.pool[i].tag is True:
                        t = [self.roundCame, self.round, self.pool[i].target]
                        self.pool[i].trace.append(t)
                        print(self.pool[i].trace)
                    self.pool[i].route[2].add_msg_in_pool(self.pool[i], env)
                    p = simpy.events.Process(env, self.pool[i].route[2].add_msg_in_pool(self.pool[i], env))
                    tr = [self.pool[i].id, env.now, self.pool[i].route[1].mix_id]
                    self.tableL2.append(tr)
                    self.delete_msg(self.pool[i])
                    k += 1
            except:
                RuntimeError
        elif self.position == 'Exit':
            i = 0
            k = 0
            try:
                while k < int(0.7 * self.bandwidth):
                    i = random.randint(0, len(self.pool))
                    self.computeProba(self.pool[i])
                    if self.pool[i].tag is True:
                        t = [self.roundCame, self.round, self.pool[i].target]
                        self.pool[i].trace.append(t)
                        print(self.pool[i].trace)
                    self.computeEntropy(self.pool[i])
                    tr = [self.pool[i].id, env.now, self.pool[i].route[2].mix_id, self.pool[i].target]
                    self.tableL3.append(tr)
                    self.delete_msg(self.pool[i])
                    k += 1
            except:
                RuntimeError

        else:
            pass

    def delete_msg(self, msg):
        if msg in self.pool:
            self.pool.remove(msg)
        else:
            pass

    def computeProba(self, msg):
        if not self.corrupt:
            msg.target = self.prob / self.bandwidth
        else:
            pass

    def computeEntropy(self, msg):
        if msg.target == 0:
            pass
        else:
            self.entropy = self.entropy + msg.target * np.log2(msg.target)
