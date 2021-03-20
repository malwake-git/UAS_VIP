import time
import signal
import sys
import json
import logging
import argparse
import numpy as np
from typing import Dict
from threading import Timer
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
import pandas as pd

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
from cflib.positioning.motion_commander import MotionCommander
from cflib.utils.multiranger import Multiranger


# URI to the Crazyflie to connect to
uri = 'radio://0/80/2M/E7E7E7E715'
URI = 'radio://0/80/2M/E7E7E7E715'
# Only output errors from the logging framework
logging.basicConfig(level=logging.ERROR)

def is_close(range):
    MIN_DISTANCE = 0.2  # m

    if range is None:
        return False
    else:
        return range < MIN_DISTANCE

def simple_log(scf, logconf,x,y,z,cf):
    keep_flying = True;
    #cf = Crazyflie(rw_cache='./cache')
    with SyncCrazyflie(URI, cf=cf) as scf:
        with SyncLogger(scf, lg_stab) as logger:
            with MotionCommander(scf) as motion_commander:
                with Multiranger(scf) as multi_ranger:
                    for i in range(100):
                        
                    #while keep_flying:
                        #if is_close(multi_ranger.up):
                            #keep_flying = False
                        cf.param.set_value('posCtlPid.zKp', '1')
                        #cf.param.set_value('posCtlPid.xKp', '1')
                        #cf.param.set_value('posCtlPid.yKp', '1')
                        #cf.param.set_value('postCtlPid.xKp','1')
                        for log_entry in logger:
                            #cf.param.set_value('posCtlPid.xKp', '1')
                            #cf.param.set_value('posCtlPid.yKp', '1')
                            cf.param.set_value('posCtlPid.zKp', '1')
                            motion_commander.start_linear_motion(0, 0, 0.05)
                            timestamp = log_entry[0]
                            data = log_entry[1]
                            logconf_name = log_entry[2]
                            count = 1
                            for i in data.values():
                                if count == 1:
                                    x.append(i)
                                elif count == 2:
                                    y. append(i)
                                else:
                                    z.append(i)
                                count = count + 1;
                                
                            print('[%d][%s]: %s' % (timestamp, logconf_name, data))
                            break
                        time.sleep(0.1)
                    motion_commander.stop()
                    return(x,y,z)
...

if __name__ == '__main__':
    # Initialize the low-level drivers (don't list the debug drivers)
    cflib.crtp.init_drivers(enable_debug_driver=True)
    x = []
    y= []
    z = []
    
    lg_stab = LogConfig(name='Stabilizer', period_in_ms=10)
    lg_stab.add_variable('stabilizer.roll', 'float')
    lg_stab.add_variable('stabilizer.pitch', 'float')
    lg_stab.add_variable('stabilizer.yaw', 'float')
    cf = Crazyflie(rw_cache='./cache')

    with SyncCrazyflie(uri, cf=cf) as scf:
        x,y,z = simple_log(scf, lg_stab,x,y,z,cf)
        #break

    z = [float(i) for i in z]
    print(z)
    #plt.plot(range(len(z)),z)
    #plt.show()
    #plt.plot(range(len(z)),z)
    #time.sleep(0.1)
    print('Demo terminated!')
    #motion_commander.stop()
    #mc.stop()
    #plt.show()
    #df = pd.DataFrame(x,y,z)
    #df.to_csv('/home/kali/Desktop/UAS_project/hw4_pid_tuning-malwake-git/x_y_z.csv')
