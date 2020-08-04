class Message:
    def __init__(self, id, type, sender, senderID, receiver, delayC, route, delay, target, tag, trace):
        self.id = "%d_%d" % (senderID, id)
        self.type = type
        self.delayC = delayC
        self.sender = sender
        self.senderID = senderID
        self.receiver = receiver
        self.route = route
        self.delay = delay
        self.target = target
        self.trace = trace
        self.tag = tag
