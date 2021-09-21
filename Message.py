class Message:
    def __init__(self, id, type, sender, route, delay, target, tag):
        self.id = "%d_%d" % (sender.id, id)
        self.type = type  # Dummy or Real packet
        self.sender = sender  # sender object
        self.route = route  # e.g. [S1, mix1, mix2, mix3, R5]
        self.delay = delay  # list of delays at 3 nodes
        self.target = target  # probability of this message being the target message
        self.tag = tag  # True if this message is a target message
        self.timeLeft = 0
        self.nextStopIndex = 1
