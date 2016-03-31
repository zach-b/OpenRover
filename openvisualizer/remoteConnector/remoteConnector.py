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
import json

from openvisualizer.eventBus      import eventBusClient
from openvisualizer.moteState     import moteState
from pydispatch import dispatcher


class remoteConnector(eventBusClient.eventBusClient):


    def __init__(self, PCip='localhost', PCport=50000):

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

        eventBusClient.eventBusClient.__init__(
            self,
            name             = self.name,
            registrations =  [
                {
                    'sender'   : self.WILDCARD,
                    'signal'   : 'fromMote.*',
                    'callback' : self._sendToRemote_handler,
                },
                {
                    'sender'   : self.WILDCARD,
                    'signal'   : 'latency',
                    'callback' : self._sendToRemote_handler,
                },
            ]
        )

        t = threading.Thread(target=self._recvdFromRemote)
        t.setDaemon(True)
        t.start()
        print 'subscriber started'



    #======================== eventBus interaction ============================
    def _printer(self, sender, signal, data):
        print 'sender : {0}, signal : {1}, data : {2}'.format(sender, signal, data)

    def _sendToRemote_handler(self,sender,signal,data):

        self.publisher.send_json({'sender' : sender, 'signal' : signal, 'data':data})
        self.printer(sender,signal,data)

    def _recvdFromRemote(self):
        while True:
            event = self.subscriber.recv_json()
            print "\nReceived remote event\n"+json.dumps(event)+"\nDispatching to event bus"
            #Beware of the unicode-utf8 encoding on python2.7
            dispatcher.send(signal=event['signal'].encode("utf8"), sender=event['sender'].encode("utf8"), data=event['data'])

    #======================== public ==========================================

    def quit(self):
        raise NotImplementedError()

    def addRaspi(self, ip):
        self.iplist.append(ip)


