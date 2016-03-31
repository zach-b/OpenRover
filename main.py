import os
import logging
import signal
import threading

log = logging.getLogger('openVisualizerApp')

from openvisualizer.moteProbe     import moteProbe
from openvisualizer.remoteConnector import remoteConnector
import coapserver
from twisted.internet import reactor



class OpenVisualizerApp(object):
    '''
    Provides an application model for OpenVisualizer. Provides common,
    top-level functionality for several UI clients.
    '''

    def __init__(self):
        # local variables
        # in "hardware" mode, motes are connected to the serial port
        self.moteProbes       = [
               moteProbe.moteProbe(serialport=p) for p in moteProbe.findSerialPorts()
        ]
        self.remoteConnector = None


    #======================== public ==========================================

    def close(self):
        '''Closes all thread-based components'''

        log.info('Closing OpenVisualizer')
        for probe in self.moteProbes:
            probe.close()
        if self.remoteConnector :
            self.remoteConnector.close()

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

    def startRemoteConnector(self, PCip, PCport):
        '''Start the remote connection when infos received by coap server

        :param PCip : ip of the central computer
        :param PCport : port of the connection
        '''
        self.remoteConnector = remoteConnector.remoteConnector(app=self, PCip=PCip, PCport=PCport)


# ======================== main ==========================================

import logging.config
logging.config.fileConfig('logging.conf')
# log
log.info('Initializing OpenVisualizerApp')
#===== start the app
app      = OpenVisualizerApp()
#===== start the coap server
coapsrv = coapserver.coapServer(app)
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



