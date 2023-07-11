"""
This example shows how to use pycromanager to interact with the micro-manager core.
Aside from the setup section, each following section can be run independently
"""
from pycromanager import Bridge
import numpy as np
import time

#### Setup ####

bridge = Bridge()
core = bridge.get_core()

for i in range(0,30,4):
        core.set_property('RCM', 'Laser 1 Power', 10.0+i)
        laser = core.get_property('RCM', 'Laser 1 Power')
        print(f"Increased by {i}, currently reads {laser}")
        time.sleep(1)

bridge.close()