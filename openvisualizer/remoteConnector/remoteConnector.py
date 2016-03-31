# Copyright (c) 2010-2013, Regents of the University of California.
# All rights reserved.
#
# Released under the BSD 3-Clause license as published at the link below.
# https://openwsn.atlassian.net/wiki/display/OW/License
import logging
log = logging.getLogger('remoteConnector')
log.setLevel(logging.ERROR)
log.addHandler(logging.NullHandler())

import threading
import zmq

from pydispatch import dispatcher


class remoteConnector():


    def __init__(self, app, PCip='localhost', PCport=50000):

        # log
        log.info("creating instance")

        # local variables
        self.stateLock                 = threading.Lock()
        self.networkPrefix             = None
        self._subcribedDataForDagRoot  = False
        self.PCip                      = PCip
        self.PCport                    = PCport


        self.context = zmq.Context()
        self.publisher = self.context.socket(zmq.PUB)
        self.publisher.bind("tcp://*:50000")
        print 'publisher started'

        self.subscriber = self.context.socket(zmq.SUB)
        self.subscriber.connect("tcp://%s:%s" % (self.PCip, self.PCport))
        self.subscriber.setsockopt(zmq.SUBSCRIBE, "")

        # give this thread a name
        self.name = 'remoteConnector'

        for mote in app.getMoteProbes() :
            # subscribe to dispatcher
            dispatcher.connect(
                self._sendToRemote_handler,
                signal = 'fromMoteProbe@'+mote.getPortName(),
            )

        self.t = threading.Thread(target=self._recvdFromRemote)
        self.t.setDaemon(True)
        self.t.start()
        print 'subscriber started'



    #======================== dispatcher interaction ============================
    def _printer(self, sender, signal, data):
        print 'sender : {0}, signal : {1}, data : {2}'.format(sender, signal, data)

    def _sendToRemote_handler(self,sender,signal,data):
        self.publisher.send_json({'sender' : sender, 'signal' : signal, 'data':data})
        self._printer(sender,signal,data)

    def _recvdFromRemote(self):
        while True:
            event = self.subscriber.recv_json()
            print "\nReceived remote event\n"+event['data'].decode("hex")+"\nDispatching to event bus"
            #Beware of the unicode-utf8 encoding on python2.7
            dispatcher.send(signal=event['signal'].encode("utf8"), sender=event['sender'].encode("utf8"), data=event['data'].decode("hex"))

    #======================== public ==========================================

    def quit(self):
        return

    def addRaspi(self, ip):
        self.iplist.append(ip)


