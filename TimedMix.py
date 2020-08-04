from util import sample_from_exp_dist
from operator import itemgetter

import simpy
import numpy as np
from numpy import random
from Message import Message

DEFAULT_SENDING_RATE = 0.1


class TimedMix:
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
    # For DRopped Messages
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
        self.env2 = simpy.Environment()

    def add_msg_in_pool(self, msg, dd):
        event66 = simpy.events.Timeout(self.env2, delay=1)
        yield event66
        now = dd + self.env2.now
        self.ctr += 1
        self.pool.append(msg)
        now = dd
        tpr = [msg, now]
        self.log.append(tpr)
        if self.position == 'Entry':
            self.setup(self.env2)
            p2 = simpy.events.Process(self.env2, self.setup(self.env2))
        else:
            pass

    def setup(self, env):
        while True:
            yield self.env2.timeout(10)
            self.flush(self.env2)

    def flush(self, env):
        i = 0
        try:
            d = self.log[i][1]
            while d < self.env2.now:
                now = self.env2.now
                self.tableID1.append(self.log[i][0].id)
                self.tableL1.append(now)
                self.tableM1.append(self.log[i][0].route[0].mix_id)
                if self.position == 'Entry':
                    if self.simulation.routing == 'hopbyhop':
                        self.log[i][0].route[1] = random.choice(self.neighbors)
                    self.log[i][0].route[1].receive(self.log[i][0], now)
                    p2 = simpy.events.Process(self.env2, self.log[i][0].route[1].receive(self.log[i][0], now))
                    self.computeProba(self.log[i][0], 0)
                    self.delete_msg(self.log[i][0])
                now = self.env2.now
                self.log.pop(i)
                d = self.log[i][1]

        except:
            RuntimeError

    def receive(self, msg, delayd):
        event66 = simpy.events.Timeout(self.env2, delay=1)
        yield event66
        self.ctr += 1
        self.pool.append(msg)
        now = delayd + self.env2.now
        Temp = [msg, now]
        self.log.append(Temp)
        if self.position == 'Middle':
            self.setup2(self.env2)
            p2 = simpy.events.Process(self.env2, self.setup2(self.env2))
        else:
            pass

    def setup2(self, env):
        while True:
            yield self.env2.timeout(10)
            self.flush2(self.env2)

    def flush2(self, env):
        self.log.sort(key=lambda r: r[1])
        i = 0
        try:
            d = self.log[i][1]
            while d < self.env2.now:
                now = self.env2.now
                self.tableID2.append(self.log[i][0].id)
                self.tableL2.append(now)
                self.tableM2.append(self.log[i][0].route[1].mix_id)
                if self.simulation.routing == 'hopbyhop':
                    self.log[i][0].route[2] = random.choice(self.neighbors)
                self.log[i][0].route[2].receive2(self.log[i][0], now)
                p66 = simpy.events.Process(self.env2, self.log[i][0].route[2].receive2(self.log[i][0], now))
                self.computeProba(self.log[i][0], 1)
                self.delete_msg(self.log[i][0])
                self.log.pop(i)
                d = self.log[i][1]
        except:
            RuntimeError

    def receive2(self, msg, delayd):
        event667 = simpy.events.Timeout(self.env2, delay=1)
        yield event667
        self.ctr += 1
        self.pool.append(msg)
        now = delayd + self.env2.now
        Temp = [msg, now]
        self.log.append(Temp)
        if self.position == 'Exit':
            self.setup3(self.env2)
            p25 = simpy.events.Process(self.env2, self.setup3(self.env2))
        else:
            pass

    def setup3(self, env):
        while True:
            yield self.env2.timeout(10)
            self.flush3(self.env2)

    def flush3(self, env):
        self.log.sort(key=lambda v: v[1])
        i = 0
        try:
            d = self.log[i][1]
            while d < self.env2.now:
                self.tableID3.append(self.log[i][0].id)
                self.tableL3.append(self.env2.now)
                self.tableM3.append(self.log[i][0].route[2].mix_id)
                self.computeProba(self.log[i][0], 2)
                if self.pool[i].VectorP[2] is not None:
                    self.tableP1.append(self.pool[i].id)
                    self.tableP3.append(self.pool[i].VectorP)
                else:
                    pass
                self.delete_msg(self.log[i][0])
                self.log.pop(i)
                d = self.log[i][1]


        except:
            RuntimeError

    def congestion_drop(self, msg, env):
        tpr = [msg, env.now]
        self.poolD.append(tpr)
        self.tableMix.append(self.mix_id)
        self.tableMsg.append(msg.id)
        self.tableTime.append(env.now)

    def delete_msg(self, msg):
        if msg in self.pool:
            self.pool.remove(msg)
            self.ctr -= 1
        else:
            pass

    def computeProba(self, msg, index):
        if msg.VectorP[index] is not None:
            prob = msg.VectorP[index] / self.bandwidth
            msg.VectorP.append(prob)
        else:
            msg.VectorP.append(None)
