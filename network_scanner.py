import scapy.all as scapy
import argparse


def get_argument():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", dest="target", help="Target IP / IP range.")
    options = parser.parse_args()
    return options

def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    list_answered = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    clients_list = []
    for element in list_answered:
        clients_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}
        clients_list = [clients_dict]
    return clients_list


def print_result(result_list):
    print("IP\t\t\tMAC Address\n----------------------------------------------------")
    for client in result_list:
        print(client["ip"] + "\t\t\t" + client["mac"])


if __name__ == "__main__":
    options = get_argument()
    scan_result = scan(options.target)
    print_result(scan_result)
