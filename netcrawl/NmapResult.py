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
                "ports": self.ports.to_dict(),
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
        ip = host.childNodes[2].getAttributeNode("addr").value
        mac = host.childNodes[4].getAttributeNode("addr").value
        dns = host.childNodes[6].childNodes[1].getAttributeNode("name").value
        ports = []
        for port in host.getElementsByTagName("port"):
            proto = port.getAttributeNode("protocol").value
            num = int(port.getAttributeNode("portid").value)
            state = port.childNodes[0].getAttributeNode("state").value
            ports.append(Port(proto, num, state))
        parsed_hosts.append(Host(mac, ip, dns, ports))
    return parsed_hosts
