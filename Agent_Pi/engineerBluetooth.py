import bluetooth
import socket

UNIC_FORMAT = "utf-8"
BYTES = 1024
FALSE = '0'
TRUE = '1'
#MAC = 'DC:A6:32:3F:EB:02'


def bt_scan(s):
    nearby_devices = bluetooth.discover_devices(lookup_names=False)

    for addr in nearby_devices:
        addressArray = str(addr).split('\'')
        print(addr)
        s.send(bytes(addressArray[1], UNIC_FORMAT))
        valid_mac = s.recv(BYTES).decode()
        if valid_mac == TRUE:
            return True

    s.send(bytes(FALSE, UNIC_FORMAT))
    return False

# for testing
#bt_scan()