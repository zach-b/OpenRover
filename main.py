import os
import logging
import signal
import threading
import time

log = logging.getLogger('openRoverApp')

import openRoverApp
import coapserver

# ======================== main ==========================================

import logging.config
logging.config.fileConfig('logging.conf')
# log
log.info('Initializing OpenVisualizerApp')
#===== start the app
app      = openRoverApp.OpenRoverApp()
#===== start the coap server
c = coapserver.coap.coap()
c.addResource(coapserver.pcInfo(app))
#===== add a cli (minimal) interface
banner  = []
banner += ['OpenRover']
banner += ['enter \'q\' to exit']
banner  = '\n'.join(banner)
print banner
while True:
    input = raw_input('> ')
    if input=='q':
        print 'bye bye.'
        app.close()
        os.kill(os.getpid(), signal.SIGTERM)



