import sys
import os
import logging
import json
import signal

log = logging.getLogger('openVisualizerApp')

from openvisualizer.eventBus      import eventBusMonitor
from openvisualizer.moteProbe     import moteProbe
from openvisualizer.moteConnector import moteConnector
from openvisualizer.remoteConnector import remoteConnector

class OpenVisualizerApp(object):
    '''
    Provides an application model for OpenVisualizer. Provides common,
    top-level functionality for several UI clients.
    '''

    def __init__(self):
        # local variables
        self.eventBusMonitor      = eventBusMonitor.eventBusMonitor()

        # in "hardware" mode, motes are connected to the serial port
        self.moteProbes       = [
               moteProbe.moteProbe(serialport=p) for p in moteProbe.findSerialPorts()
        ]
        print len(self.moteProbes)

        # create a moteConnector for each moteProbe
        self.moteConnectors       = [
            moteConnector.moteConnector(mp.getPortName()) for mp in self.moteProbes
        ]
        self.remoteConnector = remoteConnector.remoteConnector()

    #======================== public ==========================================

    def close(self):
        '''Closes all thread-based components'''

        log.info('Closing OpenVisualizer')
        for probe in self.moteProbes:
            probe.close()

    def refreshMotes(self, roverMotes):
        '''Connect the list of roverMotes to openvisualiser.

        :param roverMotes : list of the roverMotes to add
        '''
        for probe in self.moteProbes:
            probe.close()
        # in "hardware" mode, motes are connected to the serial port
        self.moteProbes       = [
               moteProbe.moteProbe(serialport=p) for p in moteProbe.findSerialPorts()
        ]
        # create a moteConnector for each moteProbe
        self.moteConnectors       = [
            moteConnector.moteConnector(mp.getPortName()) for mp in self.moteProbes
        ]

import logging.config
logging.config.fileConfig('logging.conf')
# log
log.info('Initializing OpenVisualizerApp')
#===== start the app
app      = OpenVisualizerApp()

#===== add a cli (minimal) interface
banner  = []
banner += ['OpenVisualizer']
banner += ['enter \'q\' to exit']
banner  = '\n'.join(banner)
print banner
while True:
    input = raw_input('> ')
    if input=='q':
        print 'bye bye.'
        app.close()
        os.kill(os.getpid(), signal.SIGTERM)


