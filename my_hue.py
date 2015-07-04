#!/usr/bin/python
from phue import Bridge
from ouimeaux.environment import Environment
from ouimeaux.signals import statechange, receiver
import json

class MyLights():
    def __init__(self):
        self.b = Bridge('192.168.1.2')
        # If the app is not registered and the button is not pressed, press the button and call connect() (this only needs to be run a single time)
        #self.b.connect()
        self.env = Environment()
        self.env.start()
        self.env.discover(5)

    def get_current_state(self):
        # Get the bridge state (This returns the full dictionary that you can explore)
        self.b.get_api()

        current_state = {}

        wemo_lights = self.env.list_switches()
        for wemo_light in wemo_lights:
            current_state[wemo_light] = {}
            current_state[wemo_light]['type'] = 'wemo'
            #current_state[wemo_light]['']
            current_state[wemo_light]['state'] = self.env.get_switch(wemo_light).get_state()


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

    def save_current_scene(self, scene_name):
        scenes = self.load_scenes()
        # Get the current state of the lights
        current_scene = self.get_current_state()
        # Save the current state into the dictionary
        scenes[scene_name] = current_scene
        # Write it all out
        with open('scenes.json', 'w') as fp:
            json.dump(scenes, fp, sort_keys=True, indent=4, separators=(',', ': '))

    def load_scenes(self):
        with open('scenes.json', 'r') as fp:
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


if __name__ == '__main__':
    ml = MyLights()
    ml.set_scene('off')
    #ml.save_current_scene('off')
    