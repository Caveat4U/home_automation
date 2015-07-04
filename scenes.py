#!/usr/bin/python
from phue import Bridge
from ouimeaux.environment import Environment
from ouimeaux.signals import statechange, receiver
import json
from abc import ABCMeta,abstractmethod
from os.path import exists as file_exists
import threading

class MyLights(threading.Thread):
    __metaclass__ = ABCMeta
    def __init__(self, light_type = ""):
        threading.Thread.__init__(self)
        self._light_type = ''
        self.outfile = "%s_scenes.json"
        self.light_type = light_type

    @abstractmethod
    def run(self):
        pass

    @property
    def light_type(self):
        return self._light_type

    @light_type.setter
    def light_type(self, value):
        self.outfile = self.outfile % value
        self._light_type = value

    @abstractmethod
    def get_current_state(self):
        pass

    def save_current_scene(self, scene_name):
        scenes = self.load_scenes()
        # Get the current state of the lights
        current_scene = self.get_current_state()
        # Save the current state into the dictionary
        scenes[scene_name] = current_scene
        # Write it all out
        with open(self.outfile, 'w') as fp:
            json.dump(scenes, fp, sort_keys=True, indent=4, separators=(',', ': '))

    def load_scenes(self):
        if not file_exists(self.outfile):
            print "Could not find the '%s' file." % self.outfile
            return {}
        with open(self.outfile, 'r') as fp:
            if fp.read():
                fp.seek(0)
                scenes = json.load(fp)
            else:
                print "Could not find contents in the .json file."
                return {}
        return scenes

    def load_scene(self, scene_name = 'cool'):
        return self.load_scenes().get(scene_name, {})

    def set_scene(self, scene_name='cool'):
        # Load the scene into active memory
        scene = self.load_scene(scene_name)
        if self.light_type == 'phue':
            # Get the lights so I can interact with them by name
            phue_lights = self.b.get_light_objects('name')
        
        for light_name, light in scene.items():
            if light['type'] == 'phue':
                this_light = phue_lights[light_name]
                if 'brightness' in light:
                    this_light.brightness = light['brightness']
                if 'on' in light:
                    this_light.on = light['on']
                if 'saturation' in light:
                    this_light.saturation = light['saturation']
                if 'hue' in light:
                    this_light.hue = int(light['hue'], 16)
                this_light.transitiontime = 0
            elif light['type'] == 'wemo':
                self.env.get_switch(light_name).set_state(light['state'])
            else:
                print "type undefined for %s" % light_name

class WemoLights(MyLights):
    def __init__(self):
        super(WemoLights, self).__init__('wemo')
        
    def run(self):
        self.env = Environment()
        self.env.start()
        self.env.discover(10)

    def get_current_state(self):
        current_state = {}
        wemo_lights = self.env.list_switches()
        if len(wemo_lights) == 0:
            print "No wemo lights were discovered"
        for wemo_light in wemo_lights:
            current_state[wemo_light] = {}
            current_state[wemo_light]['type'] = 'wemo'
            current_state[wemo_light]['state'] = self.env.get_switch(wemo_light).get_state()
        return current_state

class PhueLights(MyLights):
    def __init__(self):
        super(PhueLights, self).__init__('phue')

    def run(self):
        self.b = Bridge('192.168.1.2')
        # If the app is not registered and the button is not pressed, press the button and call connect() (this only needs to be run a single time)
        #self.b.connect()

    def get_current_state(self):
        # Get the bridge state (This returns the full dictionary that you can explore)
        self.b.get_api()

        current_state = {}

        for l in  self.b.lights:
            name = l.name
            current_state[name] = {}
            current_state[name]['type'] = 'phue'
            current_state[name]['brightness'] = l.brightness
            current_state[name]['on'] = l.on
            try:
                current_state[name]['saturation'] = l.saturation
                current_state[name]['hue'] = hex(l.hue)
                current_state[name]['transitiontime'] = l.transitiontime
            except KeyError,e:
                pass # No key found
        return current_state


if __name__ == '__main__':
    p = PhueLights()
    w = WemoLights()
    light_pool = [p,w]

    # Kick off the threads
    [t.start() for t in light_pool]
    

    scene_name = 'cool'
    #[light_set.save_current_scene(scene_name) for light_set in light_pool]
    [light_set.set_scene(scene_name) for light_set in light_pool]

    # Wait for all threads to complete
    for t in light_pool:
        t.join()
    