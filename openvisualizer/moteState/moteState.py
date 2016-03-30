# Copyright (c) 2010-2013, Regents of the University of California. 
# All rights reserved. 
#  
# Released under the BSD 3-Clause license as published at the link below.
# https://openwsn.atlassian.net/wiki/display/OW/License
'''
Contains the moteState container class, as well as contained classes that
structure the mote data. Contained classes inherit from the abstract
StateElem class.
'''
import logging
log = logging.getLogger('moteState')
log.setLevel(logging.ERROR)
log.addHandler(logging.NullHandler())

import copy
import time
import threading
import json

from openvisualizer.moteConnector import ParserStatus
from openvisualizer.eventBus      import eventBusClient

class moteState(eventBusClient.eventBusClient):
    
    ST_OUPUTBUFFER      = 'OutputBuffer'
    ST_ASN              = 'Asn'
    ST_MACSTATS         = 'MacStats'
    ST_SCHEDULEROW      = 'ScheduleRow'
    ST_SCHEDULE         = 'Schedule'
    ST_BACKOFF          = 'Backoff'
    ST_QUEUEROW         = 'QueueRow'
    ST_QUEUE            = 'Queue'
    ST_NEIGHBORSROW     = 'NeighborsRow'
    ST_NEIGHBORS        = 'Neighbors'
    ST_ISSYNC           = 'IsSync'
    ST_IDMANAGER        = 'IdManager'
    ST_MYDAGRANK        = 'MyDagRank'
    ST_KAPERIOD         = 'kaPeriod'
    ST_ALL              = [
        ST_OUPUTBUFFER,
        ST_ASN,
        ST_MACSTATS,
        ST_SCHEDULE,
        ST_BACKOFF,
        ST_QUEUE,
        ST_NEIGHBORS,
        ST_ISSYNC,
        ST_IDMANAGER, 
        ST_MYDAGRANK,
        ST_KAPERIOD,
    ]
    
    TRIGGER_DAGROOT     = 'DAGroot'
    SET_COMMAND         = 'imageCommand'

    # command for golen image:        command,       id length
    COMMAND_SET_EBPERIOD          =  ['ebPeriod',     0, 1]
    COMMAND_SET_CHANNEL           =  ['channel',      1, 1]
    COMMAND_SET_KAPERIOD          =  ['kaPeriod',     2, 2]
    COMMAND_SET_DIOPERIOD         =  ['dioPeriod',    3, 2]
    COMMAND_SET_DAOPERIOD         =  ['daoPeriod',    4, 2]
    COMMAND_SET_DAGRANK           =  ['dagrank',      5, 2]
    COMMAND_SET_SECURITY_STATUS   =  ['security',     6, 1]
    COMMAND_SET_FRAMELENGTH       =  ['frameLength',  7, 2]
    COMMAND_SET_ACK_STATUS        =  ['ackReply',     8, 1]
    COMMAND_SET_6P_ADD            =  ['6pAdd',        9, 3]
    COMMAND_SET_6P_DELETE         =  ['6pDelete',    10, 3]
    COMMAND_SET_6P_COUNT          =  ['6pCount',     11, 0]
    COMMAND_SET_6P_LIST           =  ['6pList',      12, 0]
    COMMAND_SET_6P_CLEAR          =  ['6pClear',     13, 0]
    COMMAND_SET_SLOTDURATION      =  ['slotDuration',14, 2]
    COMMAND_SET_6PRESPONSE_STATUS =  ['response',    15, 1]
    COMMAND_ALL                   = [
        COMMAND_SET_EBPERIOD ,
        COMMAND_SET_CHANNEL,
        COMMAND_SET_KAPERIOD,
        COMMAND_SET_DIOPERIOD,
        COMMAND_SET_DAOPERIOD,
        COMMAND_SET_DAGRANK,
        COMMAND_SET_SECURITY_STATUS,
        COMMAND_SET_FRAMELENGTH,
        COMMAND_SET_ACK_STATUS,
        COMMAND_SET_6P_ADD,
        COMMAND_SET_6P_DELETE,
        COMMAND_SET_6P_COUNT,
        COMMAND_SET_6P_LIST,
        COMMAND_SET_6P_CLEAR,
        COMMAND_SET_SLOTDURATION,
        COMMAND_SET_6PRESPONSE_STATUS
    ]

    TRIGGER_ALL         = [
        TRIGGER_DAGROOT,
    ]