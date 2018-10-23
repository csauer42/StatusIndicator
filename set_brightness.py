#!/usr/bin/env python

import sys
import serial

if len(sys.argv) != 2:
    print("Usage: ./set_brightness.py [int value 0-15]")
    sys.exit(1)

try:
    val = int(sys.argv[1])
except ValueError:
    print("Invalid value")
    sys.exit(1)

if val < 0 or val > 15:
    print("Invalid value")
    sys.exit(1)

message = bytearray(5)
message[3] = val
message[4] = ord('\n')

ser = serial.Serial('/dev/ttyACM0')
ser.write(message)
ser.close()
