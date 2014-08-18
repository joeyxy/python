#!/usr/bin/env python2
# This file is part of Weevely NG.
#
# Copyright(c) 2011-2012 Weevely Developers
# http://code.google.com/p/weevely/
#
# This file may be licensed under the terms of of the
# GNU General Public License Version 2 (the ``GPL'').
#
# Software distributed under the License is distributed
# on an ``AS IS'' basis, WITHOUT WARRANTY OF ANY KIND, either
# express or implied. See the GPL for the specific language
# governing rights and limitations.
#
# You should have received a copy of the GPL along with this
# program. If not, go to http://www.gnu.org/licenses/gpl.html
# or write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.


from core.terminal import Terminal, module_trigger, help_string
from core.modulehandler import ModHandler
from core.moduleexception import ModuleException
from core.helper import banner, credits, usage

import sys
import os



if __name__ == "__main__":



    if len(sys.argv) >= 3 and (sys.argv[1].startswith('http') or sys.argv[1] == 'session'):         
        
        url = None
        password = None
        sessionfile = None

        if sys.argv[1].startswith('http'):
            url = sys.argv[1]
            password = sys.argv[2]
        else:
            sessionfile = sys.argv[2]

        try:
            
            module_handler = ModHandler(url=url, password=password, sessionfile=sessionfile)
            
            if len(sys.argv) == 3:     
                Terminal (module_handler).loop()
            else:
                Terminal(module_handler).run_cmd_line(sys.argv[3:])
    
        except ModuleException, e:
            print '[%s] [!] %s ' % (e.module, e.error)
        except (KeyboardInterrupt, EOFError):
            print '\n[!] Exiting. Bye ^^'



    elif len(sys.argv) >= 3 and sys.argv[1].startswith('generate'):

        genname = sys.argv[1]
        password = sys.argv[2]

        if genname == 'generate':
            genname = 'generate.php' 

        try:
            Terminal (ModHandler()).run_cmd_line([':%s' % genname ] + sys.argv[2:])
        except ModuleException, e:
            print '[!] [%s] %s ' % (e.module, e.error)

    elif len(sys.argv) >= 2 and sys.argv[1] == 'help':
        Terminal (ModHandler()).run_cmd_line([':help' ] + sys.argv[2:])



    elif len(sys.argv)==2 and sys.argv[1] == 'credits':
        print credits


    else:
        print banner, usage 


