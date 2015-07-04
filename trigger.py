from abc import ABCMeta,abstractmethod

class IClickerTrigger(object):
    __metaclass__ = ABCMeta
    
    def __init__(self, clicker_id, response_info, time_of_trigger, sequence_number):
        self.clicker_id = clicker_id
        self.response_info = response_info
        self.time_of_trigger = time_of_trigger
        self.sequence_number = sequence_number
        self.action()
    
    @abstractmethod
    def action(self):
        pass

class LightControl(Trigger):
    def __init__(self):
        pass