"""
Example script that allows a user to "push" the Crazyflie 2.X around
using your hands while it's hovering.

This examples uses the Flow and Multi-ranger decks to measure distances
in all directions and tries to keep away from anything that comes closer
than 0.2m by setting a velocity in the opposite direction.

The demo is ended by either pressing Ctrl-C or by holding your hand above the
Crazyflie.
"""

import time
import signal
import sys
import json
import argparse
import numpy as np
from typing import Dict

import cflib.crtp
from cflib.crazyflie.log import LogConfig
from cflib.crazyflie.swarm import CachedCfFactory
from cflib.crazyflie.swarm import Swarm
from cflib.crazyflie.syncLogger import SyncLogger
from cflib.crazyflie.mem import MemoryElement
from cflib.crazyflie.mem import Poly4D
from typing import List, Dict
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.crazyflie import Crazyflie

import logging
import sys
import time

import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.positioning.motion_commander import MotionCommander
from cflib.utils.multiranger import Multiranger

DRONE0 = 'radio://0/80/2M/E7E7E7E715'
#DRONE1 = 'radio://0/70/2M/E7E7E7E702'
#DRONE2 = 'radio://0/70/2M/E7E7E7E703'

#URI = 'radio://0/80/2M/E7E7E7E715'

trajectory_assignment = {
    0: DRONE0,
   # 1: DRONE1,
   # 2: DRONE2
}


if len(sys.argv) > 1:
    URI = sys.argv[1]

# Only output errors from the logging framework
logging.basicConfig(level=logging.ERROR)


def is_close(range):
    MIN_DISTANCE = 0.2  # m

    if range is None:
        return False
    else:
        return range < MIN_DISTANCE


if __name__ == '__main__':
    # Initialize the low-level drivers (don't list the debug drivers)
    cflib.crtp.init_drivers(enable_debug_driver=True)

    cf = Crazyflie(rw_cache='./cache')
    factory = CachedCfFactory(rw_cache='./cache')
    URI = {trajectory_assignment[key] for key in trajectory_assignment.keys()}
    #cf = scf.cf
    #for i in URI:
    #with SyncCrazyflie(URI, cf=cf) as scf:
    with Swarm(URI, factory=factory) as scf:
        with MotionCommander(scf) as motion_commander:
            with Multiranger(scf) as multi_ranger:
                keep_flying = True

                while keep_flying:
                    VELOCITY = 0.5
                    velocity_x = 0.0
                    velocity_y = 0.0

                    if is_close(multi_ranger.front):
                        velocity_x -= VELOCITY
                    if is_close(multi_ranger.back):
                        velocity_x += VELOCITY

                    if is_close(multi_ranger.left):
                        velocity_y -= VELOCITY
                    if is_close(multi_ranger.right):
                        velocity_y += VELOCITY

                    if is_close(multi_ranger.up):
                        keep_flying = False

                    ##motion_commander.start_linear_motion(
                      ##  velocity_x, velocity_y, 0)
                    motion_commander.circle_right(0.5, velocity=0.5,
                                                     angle_degrees=180)
                      
                    time.sleep(0.1)

                    print('Demo terminated!')
