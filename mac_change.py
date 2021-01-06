import subprocess
import argparse
import re

class Changer_MAC():
    def __init__(self):
        self.default_mac_eth_0 = '08:00:27:30:b0:5c'

    def get_arguments(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("-i", "--interface", dest="interface", help="Interface to change its MAC address")
        parser.add_argument("-m", "--mac", dest="new_mac", help="New MAC address")
        options = parser.parse_args()

        if not options.interface:
            parser.error("[-] Please specify an interface, use --help for more info")
        elif not options.new_mac:
            parser.error("[-] Please specify an new_mac, use --help for more info")
        elif options.new_mac == 'default':
            options.new_mac = self.default_mac_eth_0
        return options

    def change_mac(self, interface, new_mac):
        print("[+] Changing MAC address for " + interface + " to " + new_mac)
        subprocess.call(["ifconfig", interface, "down"])
        subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
        subprocess.call(["ifconfig", interface, "up"])


    def current_mac(self, interface):
        ifconfig_result = subprocess.check_output(["ifconfig", interface])
        mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result.decode("utf-8"))

        if mac_address_search_result:
            return mac_address_search_result.group(0)
        else:
            print(" [-] Could not read MAC address. ")

    def printer_result(self):
        options = self.get_arguments()

        get_current_mac = self.current_mac(options.interface)
        print("Current MAC" + str(get_current_mac))

        self.change_mac(options.interface, options.new_mac)

        get_current_mac = self.current_mac(options.interface)
        if get_current_mac == options.new_mac:
            print("[+] MAC address was successfully changed to " + get_current_mac)
        else:
            print("[-] MAC address did not get changed.")

if __name__ == "__main__":
    change_mac = Changer_MAC()
    change_mac.printer_result()
