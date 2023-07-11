"""
This example shows how to use pycromanager to interact with the micro-manager core.
Aside from the setup section, each following section can be run independently
"""
from pycromanager import Bridge
import numpy as np
import time

#### Setup ####

## docs at: https://pycro-manager--372.org.readthedocs.build/en/372/index.html

with Bridge() as bridge:

    #get object representing micro-manager core
    core = bridge.get_core()


    #### Calling core functions ###
    exposure = core.get_exposure()

    print(exposure)


    #### Setting and getting properties ####
    #Here we set a property of the core itself, but same code works for device properties
    # laser = core.get_property('RCM', 'Laser 1 Power')
    for i in range(0,30,4):
        core.set_property('RCM', 'Laser 1 Power', 10.0+i)
        laser = core.get_property('RCM', 'Laser 1 Power')
        print(f"Increased by {i}, currently reads {laser}")
        time.sleep(1)
    # print(laser)
    # core.set_property('Core', 'AutoShutter', 0)


    # #### Acquiring images ####
    # #The micro-manager core exposes several mechanisms foor acquiring images. In order to
    # #not interfere with other pycromanager functionality, this is the one that should be used
    # core.snap_image()
    # tagged_image = core.get_tagged_image()
    # #If using micro-manager multi-camera adapter, use core.getTaggedImage(i), where i is
    # #the camera index

    # #pixels by default come out as a 1D array. We can reshape them into an image
    # pixels = np.reshape(tagged_image.pix,
    #                     newshape=[tagged_image.tags['Height'], tagged_image.tags['Width']])
    # #plot it
    # plt.imshow(pixels, cmap='gray')
    # plt.show()