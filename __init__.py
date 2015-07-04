from iclickerpoll import *
from scenes import *
import signal, argparse
from os import geteuid

if geteuid() != 0:
    print "You must be root in order to use the home automation program."
    exit(1)

class HomeAutomation(object):
    def __init__(self):
        self.light_pool = None
        self.initialize_iclicker()
        self.initialize_lights()
        self.freq1 = self.freq2 = 'a'

    def initialize_lights(self):
        p = PhueLights()
        w = WemoLights()
        self.light_pool = [p,w]

        # Kick off the threads
        [t.start() for t in self.light_pool]
        return True

    def initialize_iclicker(self):
        # Initiate the polling
        print 'Finding iClicker Base' 
        base = IClickerBase()
        base.get_base()
        print 'Initializing iClicker Base'
        base.initialize(self.freq1, self.freq2)
        poll = IClickerPoll(base)
        
    def set_scene(scene_name = 'cool'):      
        #[light_set.save_current_scene(scene_name) for light_set in light_pool]
        [light_set.set_scene(scene_name) for light_set in light_pool]

    def __del__():
        # Wait for all threads to complete
        for t in light_pool:
            t.join()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Start your home up Chris...')
    parser.add_argument('--debug', action='store_true', default=False,
    args = parser.parse_args()
    # Process all the arguments
    #if args.debug:
    #    log.setLevel(0)
    my_home = HomeAutomation()
