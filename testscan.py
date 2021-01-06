import kamene.all as scapy

scapy.load_module("p0f")


def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    list_answered = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    clients_list = []
    for element in list_answered:
        p0f(element[0])
        #print(element[1].show())

        #clients_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}
        #clients_list = [clients_dict]
    #return clients_list

scan("192.168.0.1/24")
