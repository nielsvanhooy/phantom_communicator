from netaddr import AddrFormatError, IPAddress, IPNetwork


def create_cidr_notation(subnet, mask):
    try:
        cidr = IPNetwork(f"{subnet}/{mask}").prefixlen
        # ex:  10.0.0.0/24
        return f"{subnet}/{cidr}"
    except AddrFormatError:
        return "0.0.0.0"


def check_if_ip_in_network(ipaddress, network, subnet_mask):
    cidr = create_cidr_notation(network, subnet_mask)
    return IPAddress(ipaddress) in IPNetwork(cidr)
