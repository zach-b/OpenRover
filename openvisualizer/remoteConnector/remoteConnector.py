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
import socket
import traceback
import sys
import openvisualizer.openvisualizer_utils as u
import zmq
import time

from openvisualizer.eventBus      import eventBusClient
from openvisualizer.moteState     import moteState


class remoteConnector(eventBusClient.eventBusClient):

    def __init__(self, iplist=[]):

        # log
        log.info("creating instance")

        # local variables
        self.stateLock                 = threading.Lock()
        self.networkPrefix             = None
        self._subcribedDataForDagRoot  = False
        self.iplist = iplist

        self.context = zmq.Context()
        self.publisher = self.context.socket(zmq.PUB)
        self.publisher.bind("tcp://*:50000")
        print 'publisher started'


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


    #======================== eventBus interaction ============================

    def _sendToRemote_handler(self,sender,signal,data):

        self.publisher.send_json({'sender' : sender, 'signal' : signal, 'data':data})
        print 'msg sent'



    #======================== public ==========================================

    def quit(self):
        raise NotImplementedError()

    def addRaspi(self, ip):
        self.iplist.append(ip)
