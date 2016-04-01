import logging
import time

log = logging.getLogger('openVisualizerApp')

from openvisualizer.moteProbe     import moteProbe
from openvisualizer.remoteConnector import remoteConnector



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

    def startRemoteConnector(self, PCip, PCport, roverID):
        '''Start the remote connection when infos received by coap server

        :param PCip : ip of the central computer
        :param PCport : port of the connection
        '''
        if self.remoteConnector :
            self.remoteConnector.close()
            #leave it time to timeout
            time.sleep(1)
            self.remoteConnector=None
        self.remoteConnector = remoteConnector.remoteConnector(app=self, PCip=PCip, PCport=PCport, roverID=roverID)