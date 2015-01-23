# -*- coding: utf-8 -*-

"""

pyfellowshipone API library

"""

__title__ = 'pyfellowshipone'
__version__ = '0.0.1'
__author__ = 'Erick Pece'

import logging

import logging
try:  # Python 2.7+
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

logging.getLogger(__name__).addHandler(NullHandler())