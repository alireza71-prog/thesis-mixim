from random import sample
from Client import Client
from Mix import Mix

flushed = False  # True if a mix has flushed since the beginning of the simulation


class Pool(Mix):
    # For dropped Messages
    tableMsg = []
    tableTime = []
    tableMix = []
    flushed = flushed

    def __init__(self, mix_id, simulation, position,capacity,pool_size, Fpercent,numberTargets, corrupt, prob):
        super().__init__(mix_id, simulation, position, capacity, numberTargets, corrupt)

        self.pool = []
        self.prob= prob
        self.neighbors = []  # mixes in next layer used if routing == 'hopbyhop'
        self.pool_size = pool_size  # pool threshold
        self.flushPercent = Fpercent
        self.round = 0

    def receive_msg(self, msg):
        msg.nextStopIndex += 1
        self.pool.append(msg)
        for i in range(0, self.numberTargets):
            self.Pmix[i] += msg.target[i]
        if msg.type == 'Real' or msg.type == 'ClientDummy':
            self.NumberOfrealMessages += 1
        if msg.tag and self.simulation.printing:
            print(
                f'Target message arrived at mix {self.id} at time {self.env.now} and size of the pool{len(self.pool)}')
        if len(self.pool) >= self.pool_size:
            self.flush()
            self.round +=1
            self.simulation.numberrounds.append(self.round)
            self.simulation.stableMix = True
            for i in range(9):
                self.simulation.setStableMix(i)



    def flush(self):
        flushAmount = int(self.flushPercent * self.pool_size)
        flushingList = sample(self.pool, k=flushAmount)
        effectivePoolSize = len(list(filter(lambda x: x.type != 'Malicious Dummy', flushingList)))


        for message in flushingList:
            self.computeProba(message, effectivePoolSize)
            if not isinstance(message.route[message.nextStopIndex], Client) and message.route[message.nextStopIndex] is None:
                # not the last mix, for hop by hop routing
                message.route[message.nextStopIndex] = sample(self.neighbors, k=1)[0]

            nextStop = message.route[message.nextStopIndex]
            self.pool.remove(message)
            self.env.process(self.simulation.attacker.relay(message, nextStop, self))

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

