import subprocess
import argparse
import re


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--interface", dest="interface", help="Interface to change its MAC address")
    parser.add_argument("-m", "--mac", dest="new_mac", help="New MAC address")
    options = parser.parse_args()

    if not options.interface:
        parser.error("[-] Please specify an interface, use --help for more info")
    elif not options.new_mac:
        parser.error("[-] Please specify an new_mac, use --help for more info")
    return options


def change_mac(interface, new_mac):
    print("[+] Changing MAC address for " + interface + " to " + new_mac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call("ifconfig", interface, "hw", "ether", new_mac)
    subprocess.call(["ifconfig", interface, "up"])


def current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", options.interface])
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)

    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print(" [-] Could not read MAC address. ")


if __name__ == "__main__":
    options = get_arguments()

    get_current_mac = current_mac(options.interface)
    print("Current MAC" + str(get_current_mac))

    change_mac(options.interface, options.new_mac)

    get_current_mac = current_mac(options.interface)
    if get_current_mac == options.new_mac:
        print("[+] MAC address was successfully changed to " + get_current_mac)
    else:
        print("[-] MAC address did not get changed.")
