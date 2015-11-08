#!/usr/bin/env python
# encoding: utf-8
"""
virtual_env_bootstrap_creator_example.py

Created by ngift on 2008-03-08.
Copyright (c) 2008 __MyCompanyName__. All rights reserved.
"""

import virtualenv, textwrap
output = virtualenv.create_bootstrap_script(textwrap.dedent("""
import os, subprocess
def after_install(options, home_dir):
    etc = join(home_dir, 'etc')
    if not os.path.exists(etc):
        os.makedirs(etc)
    subprocess.call([join(home_dir, 'bin', 'easy_install'),
                     'liten'])
"""))
f = open('liten-bootstrap.py', 'w').write(output)
