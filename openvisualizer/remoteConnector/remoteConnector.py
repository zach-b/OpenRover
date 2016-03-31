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
        self.PCip                      = PCip
        self.PCport                    = PCport
        self.goOn                      = True


        self.context = zmq.Context()
        self.publisher = self.context.socket(zmq.PUB)
        #Always start the publisher on the same port as the PC (choice)
        self.publisher.bind("tcp://*:{0}".format(self.PCport))
        log.info('publisher started')

        self.subscriber = self.context.socket(zmq.SUB)
        self.subscriber.connect("tcp://%s:%s" % (self.PCip, self.PCport))
        self.subscriber.setsockopt(zmq.SUBSCRIBE, "")
        #set timeout on receiving so the thread can terminate when self.goOn == False.
        self.subscriber.setsockopt(zmq.RCVTIMEO, 1000)

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
        log.info('subscriber started')


    #======================== remote interaction ============================
    def _sendToRemote_handler(self,sender,signal,data):
        self.publisher.send_json({'sender' : sender, 'signal' : signal, 'data':data})
        print ('message sent to remote host :\n sender : {0}, signal : {1}, data : {2}'.format(sender, signal, data))

    def _recvdFromRemote(self):
        while self.goOn :
            try :
                event = self.subscriber.recv_json()
                log.debug("\nReceived remote command\n"+event['data'].decode("hex")+"from sender : "+event['sender']+"\nDispatching to event bus")
                #Beware of the unicode-utf8 encoding on python2.7
                dispatcher.send(signal=event['signal'].encode("utf8"), sender=event['sender'].encode("utf8"), data=event['data'].decode("hex"))
            except zmq.Again :
                pass

    #======================== public ==========================================

    def close(self):
        self.goOn = False


