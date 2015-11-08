#!/usr/bin/env python
#uploads new router config
import netsnmp

vars = netsnmp.Varbind(netsnmp.VarList(netsnmp.Varbind(".1.2.6.1.4.1.9.2.10.6.0", "1"),
        (netsnmp.Varbind("cisco.example.com.1.3.6.1.4.1.9.2.10.12.172.25.1.1", 
                        "iso-config.bin")

result = netsnmp.snmpset(vars,
                        Version = 1,
                        DestHost='cisco.example.com',
                        Community='readWrite')




