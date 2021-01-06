import kamene.all as scapy
import argparse


class My_scan():

    def get_argument(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("-t", "--target", dest="target", help="Target IP / IP range.")
        options = parser.parse_args()
        return options

    def scan(self, ip):
        arp_request = scapy.ARP(pdst=ip)
        broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff:ff")
        arp_request_broadcast = broadcast / arp_request
        list_answered = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
        clients_list = [{"ip": element[1].psrc, "mac": element[1].hwsrc} for element in list_answered]
        return clients_list

    def print_result(self):
        options = self.get_argument()
        scan_result = self.scan(options.target)
        print("IP\t\t\tMAC Address\n----------------------------------------------------")
        for client in scan_result:
            print(client["ip"] + "\t\t\t" + client["mac"])


if __name__ == "__main__":
    my_scan = My_scan()
    my_scan.print_result()

