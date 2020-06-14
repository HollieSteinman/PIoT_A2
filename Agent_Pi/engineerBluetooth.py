import bluetooth
import socket

UNIC_FORMAT = "utf-8"
BYTES = 1024
FALSE = '0'
TRUE = '1'

# engineerBluetooth uses PyBluez:
# https://github.com/pybluez/pybluez


def bt_scan(s):
    # scan for nearby devices
    nearby_devices = bluetooth.discover_devices(lookup_names=False)

    # for each device
    for addr in nearby_devices:
        # find MAC address
        addressArray = str(addr).split('\'')
        # query with db
        s.send(bytes(addressArray[1], UNIC_FORMAT))
        valid_mac = s.recv(BYTES).decode()
        if valid_mac == TRUE:
            return True

    # send false when finished sending MAC addresses
    s.send(bytes(FALSE, UNIC_FORMAT))
    return False

