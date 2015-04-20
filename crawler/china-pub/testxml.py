#!/usr/bin/env python
from xml.etree import ElementTree

def print_node(node):
    print "====================================="
    for key,value in node.items():
        print "%s:%s" % (key, value)
    for subnode in node.getchildren():
        if subnode.tag == 'Result':
            print "%s:%s" % (subnode.tag, subnode.text)
        if subnode.tag == 'Status':
            print "%s:%s" % (subnode.tag, subnode.text)        
        #print "%s:%s" % (subnode.tag, subnode.text)

def read_xml(text = '', xmlfile = ''):
    root = ElementTree.fromstring(text)
    eitor = root.getiterator("Item")
    for e in eitor:
        print_node(e)



if __name__ == '__main__':
    read_xml(open("result.xml").read())