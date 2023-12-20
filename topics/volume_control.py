from topics.base_topic import BaseTopic

class ThisTopic(BaseTopic):
    def __init__(self):
        self.volume = 5
        self._regex_enter = 'set volume'

    def set_volume(self, volume):
        self.volume = volume

    def chat():
        return 'set volume to 1'


this_topic = ThisTopic()
this_topic.enter_topic('xxyy')