"""
Altitude PID tuning
"""
import matplotlib.pyplot as plt
import pandas as pd
import logging
import time
from threading import Timer
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.positioning.motion_commander import MotionCommander
import glob

import cflib.crtp  # noqa
from cflib.crazyflie.log import LogConfig

URI = 'radio://0/80/2M/E7E7E7E729'

def test_alt(kP, filename):
    
    # Only output errors from the logging framework
    logging.basicConfig(level=logging.ERROR)


    class LoggingExample:
        """
        Simple logging example class that logs the from a supplied
        link uri and disconnects after 5s.
        """

        def __init__(self, cf):
            """ Initialize and run the example with the specified link_uri """

            self._cf = cf
            self.data = {
                't': [],
                'motor': [],
                'z': []
            }
            self._lg_alt = LogConfig(name='Altitude', period_in_ms=10)
            self._lg_alt.add_variable('motor.m1', 'float')
            self._lg_alt.add_variable('motor.m2', 'float')
            self._lg_alt.add_variable('motor.m3', 'float')
            self._lg_alt.add_variable('motor.m4', 'float')
            self._lg_alt.add_variable('stateEstimate.z', 'float')
            try:
                self._cf.log.add_config(self._lg_alt)
                # This callback will receive the data
                self._lg_alt.data_received_cb.add_callback(self._alt_log_data)
                # This callback will be called on errors
                self._lg_alt.error_cb.add_callback(self._alt_log_error)
                # Start the logging
                self._lg_alt.start()
            except KeyError as e:
                print('Could not start log configuration,'
                      '{} not found in TOC'.format(str(e)))
            except AttributeError:
                print('Could not add log config, bad configuration.')

        def _alt_log_error(self, logconf, msg):
            """Callback from the log API when an error occurs"""
            print('Error when logging %s: %s' % (logconf.name, msg))

        def _alt_log_data(self, timestamp, data, logconf):
            """Callback from a the log API when data arrives"""
            self.data['motor'].append((data['motor.m1']
                + data['motor.m2']
                + data['motor.m3']
                + data['motor.m4']))
            self.data['z'].append(data['stateEstimate.z'])
            self.data['t'].append(timestamp)
            #print('[%d][%s]: %s' % (timestamp, logconf.name, data))

    # Initialize the low-level drivers
    cflib.crtp.init_drivers()


    # The Crazyflie lib doesn't contain anything to keep the application alive,
    # so this is where your application should do something. In our case we
    # are just waiting until we are disconnected.
    with SyncCrazyflie(URI) as scf:

        le = LoggingExample(scf.cf)

        scf.cf.param.set_value('posCtlPid.zKp', kP)


        # We take off when the commander is created
        with MotionCommander(scf) as mc:
            print('Taking off!')
            time.sleep(5)

            # We land when the MotionCommander goes out of scope
            print('Landing!')

        d = pd.DataFrame(le.data)
        d.to_csv(filename, index=False)

if __name__ == '__main__':
    #test_alt(1.0, 'test1_0.csv')

    #test_alt(1.9, 'test1_9.csv')
#
    #test_alt(2, 'test2_0.csv')

    #data = {}
    for filename in glob.glob("test2_0.csv"):
        name = filename.split('.')[0]
        data[name] = pd.read_csv(filename)
        data[name].index /= 100.0
        data[name].z.plot(label=name)
    plt.legend()
    plt.gca().set_ylim([0, 0.5])
    plt.gca().set_xlim([2.70, 10.00])
    plt.xlabel('t, sec')
    plt.ylabel('z, m')
    plt.grid()
