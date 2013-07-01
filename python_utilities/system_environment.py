# -*- coding: utf-8 -*-
# dydrmntion@gmail.com ~ 2013

import sys
import os
import site
import re


class system_environment(object):
    """context manager provides virtualenv with system site packages for the duration
    of the with statement."""
    def __init__(self):
        self.sys_path = self.get_sys_path()
        sys.path.append(self.sys_path)

    def get_sys_path(self):
        for path in [os.path.join(p, 'site-packages') for p in site._init_pathinfo()
                     if p.startswith(sys.real_prefix)]:
            if os.path.isdir(path):
                return path

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        # remove from path
        sys.path.remove(self.sys_path)
        for k, v in sys.modules.items():
            # and restore module namespace to its original state
            if hasattr(v, '__file__') and re.search(self.sys_path, v.__file__):
                del sys.modules[k]
