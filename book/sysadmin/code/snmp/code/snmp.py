#!/usr/bin/env python
import netsnmp

class Snmp(object):
    """A basic SNMP session"""
    def __init__(self,
                oid = "sysDescr",
                Version = 2,
                DestHost = "localhost",
                Community = "public"):
        self.oid = oid
        self.version = Version
        self.destHost = DestHost
        self.community = Community

    def query(self):
        """Creates SNMP query session"""
        try:
            result = netsnmp.snmpwalk(self.oid,
                                    Version = self.version,
                                    DestHost = self.destHost,
                                    Community = self.community)
        except Exception, err:
            print err
            result = None
        return result

