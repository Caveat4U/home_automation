from abc import ABCMeta,abstractmethod
from my_hue import *

# Would dynamically choose a trigger based on trigger type
def trigger_factory(trigger_type):
    return None

class Trigger(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        self.action()

    @abstractmethod
    def action(self):
        pass    

class IClickerTrigger(object): 
    def __init__(self, clicker_id, response_info, time_of_trigger, sequence_number):
        super(IClickerTrigger, self).__init__()
        self.clicker_id = clicker_id
        self.response_info = response_info
        self.time_of_trigger = time_of_trigger
        self.sequence_number = sequence_number
    
    def action(self):
        print self.response_info
        button = 'a'
        if button == 'a':
            pass