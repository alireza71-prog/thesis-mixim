from util import sample_from_exp_dist

import simpy
from numpy import random
import numpy as np
from Message import Message

DEFAULT_SENDING_RATE = 1000


class PoissonMix:
    tableL1 = []
    tableL2 = []
    tableL3 = []
    tableID1 = []
    tableID2 = []
    tableID3 = []
    tableS1 = []
    tableS2 = []
    tableM1 = []
    tableM2 = []
    tableM3 = []
    tableP1 = []
    tableP2 = []
    tableP3 = []
    tableS3 = []
    # For DRopped Messages
    tableMsg = []
    tableTime = []
    tableMix = []

    def __init__(self, mix_id, simulation, bandwidth, position, corrupt):
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
        self.prob = 0

    def add_msg_in_pool(self, msg, env):
        event2 = simpy.events.Timeout(env, delay=1)
        self.simulation.log_event("MSG_ADDED", env.now, msg.sender, self.mix_id, msg.id, msg.type)
        yield event2
        self.ctr += 1
        self.pool.append(msg)
        self.prob = self.prob + msg.target
        now = env.now
        tpr = [msg, now]
        self.log.append(tpr)
        self.send_msg(msg, env)
        p = simpy.events.Process(env, self.send_msg(msg, env))

    def send_msg(self, msg, env):
        if self.position == 'Entry':
            event3 = simpy.events.Timeout(env, delay=msg.delay[0])
            yield event3
            if msg.route[1] is None:
                msg.route[1] = random.choice(self.neighbors)
            self.computeProba(msg)
            msg.route[1].add_msg_in_pool(msg, env)
            p2 = simpy.events.Process(env, msg.route[1].add_msg_in_pool(msg, env))
            tr = [msg.id, env.now, msg.route[0].mix_id]
            self.tableL1.append(tr)
            if msg.tag is True:
                tpr = [msg.target, self.mix_id]
                msg.trace.append(tpr)
                print(msg.trace)
            msg.route[0].delete_msg(msg, env.now)
            self.simulation.log_event("MSG_dropped", env.now, msg.sender, msg.route[1].mix_id, msg.id, msg.type)
        elif self.position == 'Middle':
            event4 = simpy.events.Timeout(env, delay=msg.delay[1])
            yield event4
            if msg.route[2] is None:
                msg.route[2] = random.choice(self.neighbors)
            self.computeProba(msg)
            if msg.tag is True:
                tpr = [msg.target, self.mix_id]
                msg.trace.append(tpr)
                print(msg.trace)
            msg.route[2].add_msg_in_pool(msg, env)
            p2 = simpy.events.Process(env, msg.route[2].add_msg_in_pool(msg, env))
            tr = [msg.id, env.now, self.mix_id]
            self.tableL2.append(tr)
            msg.route[1].delete_msg(msg, env.now)
        elif self.position == 'Exit':
            event5 = simpy.events.Timeout(env, delay=msg.delay[2])
            yield event5
            self.computeProba(msg)
            tr = [msg.id, env.now, self.mix_id, msg.target, msg.tag]
            self.tableL3.append(tr)
            now = env.now
            self.computeEntropy(msg)
            msg.sender.receiveAck(msg)
            if msg.tag is True:
                tpr = [msg.target, self.mix_id]
                msg.trace.append(tpr)
                print(msg.trace)
            msg.route[2].delete_msg(msg, now)
        else:
            pass

    def delete_msg(self, msg, now):
        """print("msg %d sender%d removed at%f " % (msg.id, msg.sender, now))"""
        if msg in self.pool:
            self.pool.remove(msg)
            self.ctr -= 1
        else:
            pass

    def congestion_drop(self, msg, env):
        tpr = [msg, env.now]
        self.poolD.append(tpr)
        self.tableMix.append(self.mix_id)
        self.tableMsg.append(msg.id)
        self.tableTime.append(env.now)

    def computeProba(self, msg):
        if self.corrupt == False:
            msg.target = self.prob / len(self.pool)
            self.prob = self.prob - msg.target
        else:
            pass

    def computeEntropy(self, msg):
        if msg.target == 0:
            pass
        else:
            self.entropy = self.entropy + msg.target * np.log2(msg.target)
