from Client import Client
from random import sample
from Mix import Mix
from random import sample, choice
from Client import Client
from Mix import Mix
from numpy.random import exponential


class TimedMix(Mix):

    def __init__(self, mix_id, simulation, position,capacity, flushtime,numberTargets, corrupt,prob):
        super().__init__(mix_id, simulation,position, capacity,numberTargets, corrupt)
        self.pool = []
        self.poolD = []  # Used in congestion drop
        self.flushtime = flushtime
        self.prob = prob
        self.neighbors = set()
        self.env.process(self.flush())

    def receive_msg(self, msg):
        if not self.simulation.startAttack:  # if a mix reaches a poolsize of 5 percent higher than the average,
            var1 = self.simulation.env.now > self.flushtime  # average poolsize
            if var1:
                self.env.process(self.simulation.setStableMix(self.id - 1))
            if all(self.simulation.stableMixL1):
                for i in range(len(self.simulation.stableMix)):
                    self.simulation.setStableMix(i)
        for i in range(0, self.numberTargets):
            self.Pmix[i] += msg.target[i]
        if msg.type == 'Real' or msg.type == 'ClientDummy':
            self.NumberOfrealMessages += 1
        if msg.tag and self.simulation.printing:
            print(
                f'Target message arrived at mix {self.id} at time {self.env.now} and size of the pool{len(self.pool)}')
        msg.nextStopIndex += 1
        self.pool.append(msg)

    def flush(self):
        while True:
            yield self.env.timeout(self.flushtime)
            effectivePoolSize = len(list(filter(lambda x: x.type != 'Malicious Dummy', self.pool)))

            for msg in self.pool:
                self.computeProba(msg, effectivePoolSize)

                if not isinstance(msg.route[msg.nextStopIndex], Client) and msg.route[
                    msg.nextStopIndex] is None:  # not the last mix
                    msg.route[msg.nextStopIndex] = sample(self.neighbors, k=1)[0]

                nextStop = msg.route[msg.nextStopIndex]
                self.env.process(self.simulation.attacker.relay(msg, nextStop, self))

            self.pool.clear()
            # if not self.simulation.stableMix:  # send dummy if mix has flushed once
            #     self.simulation.stableMix = True

    def computeProba(self, msg, poolsize):
        if not self.corrupt:
            if self.uncertainMessage(msg):  # Returns False if the message is a Malicious dummy sent by the attacker and the mix is corrupted
                if self.layer == self.simulation.n_layers:
                    for i in range(0, self.numberTargets):
                        msg.target[i] = self.Pmix[i] / self.NumberOfrealMessages
                        self.Pmix[i] = self.Pmix[i] - msg.target[i]
                    self.NumberOfrealMessages -= 1

                else:
                    for j in range(0, self.numberTargets):
                        msg.target[j] = self.Pmix[j] / poolsize
                        self.Pmix[j] = self.Pmix[j] - msg.target[j]

    def sendDummies(self):
        # Should periodically add dummies to pool
        pass

    def uncertainMessage(self, msg):
        # returns True if this messages adds entropy to the attacker

        if msg.type == 'Malicious Dummy':
            return False
        if msg.type == 'Dummy':  # Iness: Comment this part out if you remember our conversation on 28/08 about
            # mix to mix dummies and corrupted mixes.
            if not isinstance(msg.route[msg.nextStopIndex], Client):
                if msg.route[msg.nextStopIndex].corrupt:
                    return False  # dummies sent to corrupt mix do not add to the effective poolsize
                    # these messages will get dropped at the corrupt mix, thus the attacker knows these
                    # could not have been the target message
        return True
