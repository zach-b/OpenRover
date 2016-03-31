import os
import logging
import signal

log = logging.getLogger('openVisualizerApp')

from openvisualizer.moteProbe     import moteProbe
from openvisualizer.remoteConnector import remoteConnector

from pydispatch import dispatcher


class OpenVisualizerApp(object):
    '''
    Provides an application model for OpenVisualizer. Provides common,
    top-level functionality for several UI clients.
    '''

    def __init__(self, PCip, PCport):
        # local variables
        # in "hardware" mode, motes are connected to the serial port
        self.moteProbes       = [
               moteProbe.moteProbe(serialport=p) for p in moteProbe.findSerialPorts()
        ]
        #connect to openvisualiser on the central computer
        self.remoteConnector = remoteConnector.remoteConnector(app=self, PCip=PCip, PCport=PCport)


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
        #self.moteConnectors       = [
        #    moteConnector.moteConnector(mp.getPortName()) for mp in self.moteProbes
        #]

    def getMoteProbes(self):
        return self.moteProbes

import logging.config
logging.config.fileConfig('logging.conf')
# log
log.info('Initializing OpenVisualizerApp')
#===== start the app
app      = OpenVisualizerApp('10.228.40.96', 50000)

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


