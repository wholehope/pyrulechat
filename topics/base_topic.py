class BaseTopic():
    def __init__(self):
        self._regex_enter = ''
    def enter_topic(self, msg: str):
        print(self._regex_enter)