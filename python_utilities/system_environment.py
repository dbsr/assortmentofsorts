# -*- coding: utf-8 -*-
# dydrmntion@gmail.com ~ 2013

import sys
import os
import site


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
