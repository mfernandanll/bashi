#!/usr/bin/env python3

# This script demonstrates the usage, capability and features of the library.
import serial
import argparse
import subprocess
import time
from datetime import datetime

from bluepy.btle import BTLEDisconnectError
from cursesmenu import *
from cursesmenu.items import *

from constants import ALERT_TYPES
from miband import miband

#Start serial communication with arduino
porta = serial.Serial("/dev/ttyACM0",9600)

parser = argparse.ArgumentParser()
parser.add_argument('-m', '--mac', required=False, help='Set mac address of the device')
parser.add_argument('-k', '--authkey', required=False, help='Set Auth Key for the device')
args = parser.parse_args()

# Try to obtain MAC from the file
try:
    with open("mac.txt", "r") as f:
        mac_from_file = f.read().strip()
except FileNotFoundError:
    mac_from_file = None

# Use appropriate MAC
if args.mac:
    MAC_ADDR = args.mac
elif mac_from_file:
    MAC_ADDR = mac_from_file
else:
    print("Error:")
    print("  Please specify MAC address of the MiBand")
    print("  Pass the --mac option with MAC address or put your MAC to 'mac.txt' file")
    print("  Example of the MAC: a1:c2:3d:4e:f5:6a")
    exit(1)

# Validate MAC address
if 1 < len(MAC_ADDR) != 17:
    print("Error:")
    print("  Your MAC length is not 17, please check the format")
    print("  Example of the MAC: a1:c2:3d:4e:f5:6a")
    exit(1)

# Try to obtain Auth Key from file
try:
    with open("auth_key.txt", "r") as f:
        auth_key_from_file = f.read().strip()
except FileNotFoundError:
    auth_key_from_file = None

# Use appropriate Auth Key
if args.authkey:
    AUTH_KEY = args.authkey
elif auth_key_from_file:
    AUTH_KEY = auth_key_from_file
else:
    print("Warning:")
    print("  To use additional features of this script please put your Auth Key to 'auth_key.txt' or pass the --authkey option with your Auth Key")
    print()
    AUTH_KEY = None
    
# Validate Auth Key
if AUTH_KEY:
    if 1 < len(AUTH_KEY) != 32:
        print("Error:")
        print("  Your AUTH KEY length is not 32, please check the format")
        print("  Example of the Auth Key: 8fa9b42078627a654d22beff985655db")
        exit(1)

# Convert Auth Key from hex to byte format
if AUTH_KEY:
    AUTH_KEY = bytes.fromhex(AUTH_KEY)

def send_notif():
    msg = "Doorbell 1"
    ty= 3
    a=[5,4,3]
    band.send_custom_alert(a[ty-1],msg)
    
def stop_notif():
    msg = "Girl Power"
    band.send_custom_alert(3,msg)
    band.waitForNotifications(1)
    band.disconnect()
    
def connect():
    success = False
    while not success:
        try:
            if (AUTH_KEY):
                band = miband(MAC_ADDR, AUTH_KEY, debug=True)
                success = band.initialize()
            else:
                band = miband(MAC_ADDR, debug=True)
                success = True
            break
        except BTLEDisconnectError:
            print('Connection to the MIBand failed. Trying out again in 3 seconds')
            time.sleep(3)
            continue
        except KeyboardInterrupt:
            print("\nExit.")
            exit()

            
    
if __name__ == "__main__":
    success = False
    while not success:
        try:
            if (AUTH_KEY):
                band = miband(MAC_ADDR, AUTH_KEY, debug=True)
                success = band.initialize()
            else:
                band = miband(MAC_ADDR, debug=True)
                success = True
            break
        except BTLEDisconnectError:
            print('Connection to the MIBand failed. Trying out again in 3 seconds')
            time.sleep(3)
            continue
        except KeyboardInterrupt:
            print("\nExit.")
            exit()

#    send_notif()

    while True:
        try:
            resposta = porta.read(5)
            resposta = resposta.decode("utf-8")
            print(resposta)
            time.sleep(0.3)
            if (int(resposta) > 10000):
                print('liga')
                send_notif()
        except KeyboardInterrupt:
            porta.close()
            band.disconnect()
            exit()
        
    
#    menu = CursesMenu("MIBand4", "Features marked with @ require Auth Key")
#    call_item = FunctionItem("Send Call/ Missed Call/Message", send_notif)
#    stop_item = FunctionItem("Stop Call", stop_notif)
#    connect_item = FunctionItem("Connect", connect)

#    menu.append_item(call_item)
#    menu.append_item(stop_item)
#    menu.append_item(connect_item)
#    menu.show()
    
    #send_notif()
