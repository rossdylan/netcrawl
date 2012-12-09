import xml.dom.minidom as dom


class Port(object):
    """
    <port protocol="tcp" portid="80"><state state="closed" reason="reset"
    reason_ttl="255"/><service name="http" method="table" conf="3"/></port>
    Represent a port on a scanned host
    """
    def __init__(self, protocol, num, state):
        self.proto = protocol
        self.num = num
        self.state = state

    def to_dict(self):
        return {
                "proto": self.proto,
                "num": self.num,
                "state": self.state,
               }


class Host(object):
    """
    Represent a host scanned by nmap
    """
    def __init__(self, mac, ip, dns, ports):
        self.ip = ip
        self.dns = dns
        self.ports = ports
        self.mac = mac

    def to_dict(self):
        return {
                "ip": self.ip,
                "dns": self.dns,
                "ports": map(lambda p: p.to_dict(),self.ports),
                "mac": self.mac
               }


def GenerateHosts(xml):
    """
    Take in a large xml blob and output a class structure representing all the
    nmap data we care about
    """
    data = dom.parseString(xml)
    hosts = data.getElementsByTagName("host")
    parsed_hosts = []
    for host in hosts:
        try:
            ip = ""
            mac = ""
            dns = ""
            if not len(host.childNodes) >= 7:
                continue
            if host.childNodes[2].hasAttribute("addr"):
                ip = host.childNodes[2].getAttributeNode("addr").value
                print ip
            if host.childNodes[4].hasAttribute("addr"):
                mac = host.childNodes[4].getAttributeNode("addr").value
                print mac
            if host.childNodes[6].childNodes[1].nodeType != 3 and len(host.childNodes[6].childNodes) >= 2 and host.childNodes[6].childNodes[1].hasAttribute("name"):
                dns = host.childNodes[6].childNodes[1].getAttributeNode("name").value
                print dns
            ports = []
            for port in host.getElementsByTagName("port"):
                proto = port.getAttributeNode("protocol").value
                num = int(port.getAttributeNode("portid").value)
                state = port.childNodes[0].getAttributeNode("state").value
                ports.append(Port(proto, num, state))
            parsed_hosts.append(Host(mac, ip, dns, ports))
        except Exception as e:
            print "EXCEPTION: " + e
    return parsed_hosts
