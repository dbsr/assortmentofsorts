# -*- coding: utf-8 -*-
# dydrmntion@gmail.com ~ 2013

import logging


console = logging.StreamHandler()

console.setLevel(logging.DEBUG)

console.setFormatter(
    logging.Formatter('%(asctime)s :: %(message)s', '%H:%M:%S')
)

logging.getLogger(__name__).setLevel(logging.DEBUG)

logging.getLogger(__name__).addHandler(console)

name = __name__
