#!/usr/bin/env python

import json
import requests
import sys

global debug

debug = 1



class zabbix_api(object):
    def __init__(self,user,password):
        self.user = user
        self.password = password
        self.api = "http://192.168.10.11:8061/zabbix/api_jsonrpc.php"
        self.auth_code=''
        self.headers = {'content-type':'application/json',}
        self.timeout = 5
        
    def login(self):
        auth_data = {
            "jsonrpc":"2.0",
            "method":"user.login",
            "params":{
                "user":self.user,
                "password":self.password
            },
            "id":0,
        }
        try:
            req = requests.post(self.api,data=json.dumps(auth_data),headers=self.headers,timeout=self.timeout)
            response = json.loads(req.content)
            if debug:print response
            if 'result' in response:
                self.auth_code = response['result']
                if debug:print self.auth_code
                return self.auth_code
            else:
                print response['error']['data']
        except Exception,e:
            print e
            
    def get_host(self):
        auth_code = self.login()
        if len(auth_code) == 0:
            print "login fail"
            sys.exit(1)
        json_data = {
            "jsonrpc":"2.0",
            "method":"host.get",
            "params":{
            "output":"extend",
            "filter":{"host":"app-master"},
            },
            "auth":auth_code,
            "id":1
        }
        
        try:
            req = requests.post(self.api, data=json.dumps(json_data),headers=self.headers,timeout=self.timeout)
            response = json.loads(req.content)
            print response
        except Exception,e:
            print e        
            
            
        
if __name__ == '__main__':
    request = zabbix_api(user="admin",password="zabbix")
    #request.login()
    request.get_host()
        
    
    

