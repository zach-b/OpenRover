from openvisualizer.eventBus      import eventBusMonitor
from openvisualizer.moteProbe     import moteProbe
from openvisualizer.moteConnector import moteConnector

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

        # create a moteConnector for each moteProbe
        self.moteConnectors       = [
            moteConnector.moteConnector(mp.getPortName()) for mp in self.moteProbes
        ]



