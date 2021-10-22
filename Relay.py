LINK_DELAY = 0.5
timeStable = 0.0
event = []  # what happens: attacker can generate malicious dummies or drop real messages
objID = []  # the id of message or mix
time = []  # time it happens


class Attacker:



    def __init__(self, simulation, numberTargets):
        self.event = event
        self.objID = objID
        self.time = time
        self.simulation = simulation
        self.var = True  # if target message should still be chosen
        self.env = self.simulation.env
        self.targetMessage = None
        self.dummiesID = 1  # keeps track of the IDs of the malicious dummies
        self.amountTarget = 0
        self.numberTargets = numberTargets
        self.timeStable = 0.0
        self.eventDict = dict()
        for mix in self.simulation.network.MixesAll:
            self.eventDict[mix] = self.env.event()  # event that triggers the target message to launch at the mix

    def relay(self, msg, receiver, sender):
        # Choose target message
        if self.simulation.mix_type == 'pool' and len(self.simulation.numberrounds)>self.simulation.n_mixes_per_layer*self.simulation.n_layers:
            self.simulation.startAttack= True
        if self.var and self.simulation.startAttack and msg.nextStopIndex == 1 and (msg.type == 'Real' or msg.type == 'ClientDummy'):
            if self.amountTarget < self.numberTargets:
                for i in range(0, self.numberTargets):
                    if i == self.amountTarget:
                        msg.target[i] = float(1.0)
                    else:
                        msg.target[i] = float(0.0)
                msg.tag = True
                self.targetMessage = msg
                self.amountTarget += 1
                if self.amountTarget == 1:
                    self.timeStable = self.env.now
                    if self.simulation.printing:
                        print("Network is stable at: ",self.timeStable)
                if self.simulation.printing:
                    print(f"Target message chosen: id={msg.id}, route={msg.route} at time= {self.env.now}")
                self.var = False
                yield self.env.timeout(2)
                self.var = True

        yield self.env.timeout(LINK_DELAY)  # 'link' delay
        receiver.receive_msg(msg)
        self.checkEndSim()

    def checkEndSim(self):  # check to end simulation logic
        if self.simulation.SimDuration <= self.env.now:
            if self.simulation.printing:
                print('Simulation duration limit reached')
            self.simulation.endEvent.succeed()  # end simulation if time has expired
        elif self.env.now >= (self.simulation.SimDuration - 1.5*self.timeStable - self.simulation.n_layers * self.simulation.mu - LINK_DELAY * self.simulation.n_layers):
            self.var = False
            self.simulation.numberTargets = self.amountTarget