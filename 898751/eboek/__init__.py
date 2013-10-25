# -*- coding: utf-8 -*-
# dydrmntion@gmail.com ~ 2013

import logging

frmt = logging.Formatter(
    '[%(asctime)s] %(levelname)-5s:: %(message)s', '%H:%M:%S'
)
ch = logging.StreamHandler()
ch.setFormatter(frmt)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(ch)
logger.propagate = False
