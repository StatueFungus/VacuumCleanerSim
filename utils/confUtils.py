#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  This file provides utilities like
#  logging and configuration options.
#

import json
from os import path
import logging

CONF = None
LOG = None


#
#   CONFIG
#
def init_config():
    """
    Loads the configuration from the
    json file under /conf and saves
    it under utils.CONF

    :returns: None
    :rtype: None

    """

    global CONF

    pth = path.dirname(path.abspath(__file__))
    pth = path.split(pth)[0]

    fpth = path.join(pth, 'conf/config.json')
    with open(fpth) as f:
        CONF = json.load(f)


def get_logger(name):
    """
    Retrieves a logger.

    :param name: The name of the logger
    :returns: The requested logger
    :rtype: logging.getLogger instance

    """
    log = logging.getLogger(name)
    log.setLevel(logging.ERROR)

    return log


def set_verbose(log):
    """
    Sets the logger logging level to INFO

    :param log: logging.getLogger instance
    :returns: None
    :rtype: None

    """
    log.setLevel(logging.INFO)


#
#   global initialization
#
init_config()
LOG = get_logger('VacuumCleanerSim')
if CONF['logging']['verbose']:
    set_verbose(LOG)
