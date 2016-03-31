'''
Created on 08-09-2012
@author: Maciej Wasilak
'''

import glob
import json
import sys
from twisted.internet import defer
from twisted.internet import reactor

import txthings.resource as resource
import txthings.coap as coap
import threading


class CoreResource(resource.CoAPResource):
    """
    Example Resource that provides list of links hosted by a server.
    Normally it should be hosted at /.well-known/core
    Resource should be initialized with "root" resource, which can be used
    to generate the list of links.
    For the response, an option "Content-Format" is set to value 40,
    meaning "application/link-format". Without it most clients won't
    be able to automatically interpret the link format.
    Notice that self.visible is not set - that means that resource won't
    be listed in the link format it hosts.
    """

    def __init__(self, root):
        resource.CoAPResource.__init__(self)
        self.root = root

    def render_GET(self, request):
        data = []
        self.root.generateResourceList(data, "")
        payload = ",".join(data)
        print payload
        response = coap.Message(code=coap.CONTENT, payload=payload)
        response.opt.content_format = coap.media_types_rev['application/link-format']
        return defer.succeed(response)


class MoteResource (resource.CoAPResource):
    def __init__(self):
        resource.CoAPResource.__init__(self)
        self.visible = True
        self.observable = True

    def render_GET(self, request):

        response = coap.Message(code=coap.CONTENT, payload=self.listmotes())
        return defer.succeed(response)

    def listmotes(self):
        serialList = glob.glob('/dev/ttyUSB*')   # Get all Serial ports
        return json.dumps([serial for serial in serialList])

class PCinfos(resource.CoAPResource):
    def __init__(self, app):
        resource.CoAPResource.__init__(self)
        self.visible = True
        self.observable = True
        self.app = app

    def render_PUT(self, request):
        try :
            PCip = request.payload.split(':')[0]
            PCport = request.payload.split(':')[1]
            roverID = request.payload.split(':')[2]
            self.app.startRemoteConnector(PCip, PCport, roverID)
        except :
            print "Unexpected error:", sys.exc_info()[0]
            pass
        response = coap.Message(code=coap.CONTENT, payload=self.listmotes())
        return defer.succeed(response)


    def listmotes(self):
        serialList = glob.glob('/dev/ttyUSB*')  # Get all Serial ports
        return json.dumps([serial for serial in serialList])


class coapServer() :
    def __init__(self, app):
        self.app = app
        root = resource.CoAPResource()
        well_known = resource.CoAPResource()
        root.putChild('.well-known', well_known)
        core = CoreResource(root)
        well_known.putChild('core', core)

        mote = MoteResource()
        root.putChild('motes', mote)

        pcinfo = PCinfos(self.app)
        root.putChild('pcinfo', pcinfo)

        endpoint = resource.Endpoint(root)
        reactor.listenUDP(coap.COAP_PORT, coap.Coap(endpoint)) #, interface="::")

        coapthread = threading.Thread(target=reactor.run, args=(False,))
        coapthread.start()

