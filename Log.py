
class Log:
    def __init__(self):
        self.sent_messages = {"MessageID": [], "MessageType": [], "MessageTimeLeft" :[], "MessageDelay": [], "MessageRoute" :[]}
        self.received_messages = {"MessageID": [], "MessageType": [], "MessageTimeLeft" :[],"MessageTimeReceived":[], "MessageDelay": [], "MessageRoute" :[],"MessageTarget" : [],"PrS1": [], "PrS2": [], "RealSender": [] }
        self.dummy_messages = {"DroppingNode":[],"DummyID": [], "DummyType": [], "DummyTimeLeft" :[], "DummyDelay": [], "DummyRoute" :[], "DummyPr":[]}
        self.mix_data = {"MessageID": [], "MessageType": [],"MessageTag": [], "MessageTarget": [],"MessageTime_L": [], "MessageTime_R": [], "Len": []}
        self.messages_indis = {"MessageID": [],"PrS1": [], "PrS2": [], "RealSender": [], "Sampling": []}
    def Dummies_Dropped_end_link(self, dummy, dropping_node):
        self.dummy_messages["DroppingNode"].append(dropping_node)
        self.dummy_messages["DummyID"].append(dummy.id)
        self.dummy_messages["DummyType"].append(dummy.type)
        self.dummy_messages["DummyTimeLeft"].append(dummy.timeLeft)
        self.dummy_messages["DummyDelay"].append(dummy.delay)
        self.dummy_messages["DummyRoute"].append(dummy.route)
        self.dummy_messages["DummyPr"].append(dummy.target)

    def SentMessage(self, msg):
        self.sent_messages["MessageID"].append(msg.id)
        self.sent_messages["MessageType"].append(msg.type)
        self.sent_messages["MessageTimeLeft"].append(msg.timeLeft)
        self.sent_messages["MessageDelay"].append(msg.delay)
        self.sent_messages["MessageRoute"].append(msg.route)

    def ReceivedMessage(self, msg):

        self.received_messages["MessageID"].append(msg.id)
        self.received_messages["MessageType"].append(msg.type)
        self.received_messages["MessageTimeLeft"].append(msg.timeLeft)
        self.received_messages["MessageTimeReceived"].append(msg.timeReceived)
        self.received_messages["MessageDelay"].append(msg.delay)
        self.received_messages["MessageRoute"].append(msg.route)
        self.received_messages["MessageTarget"].append(msg.target)
        self.received_messages["PrS1"].append(msg.sender_estimate[0])
        self.received_messages["PrS2"].append(msg.sender_estimate[1])
        self.received_messages["RealSender"].append(msg.sender.id)
    def MessagesLD(self, msg):
        if msg.sampling:
            self.messages_indis["MessageID"].append(msg.id)
            self.messages_indis["PrS1"].append(msg.sender_estimate[0])
            self.messages_indis["PrS2"].append(msg.sender_estimate[1])
            self.messages_indis["RealSender"].append(msg.sender.id)
            self.messages_indis["Sampling"].append(msg.sampling)
        else:
            pass

    def MixData(self, msg, time_left, nbr):
        self.mix_data["MessageID"].append(msg.id)
        self.mix_data["MessageType"].append(msg.type)
        self.mix_data["MessageTarget"].append(msg.tablePr)
        self.mix_data["MessageTag"].append(msg.tag)
        self.mix_data["MessageTime_L"].append(time_left)
        self.mix_data["MessageTime_R"].append(msg.time_received)
        self.mix_data["Len"].append(nbr)
