#!/usr/bin/env python

import sys
import serial

if len(sys.argv) != 2:
    print("Usage: ./test.py [string]")
    sys.exit(1)

dstr = sys.argv[1]

if len(dstr) > 4:
    dstr = dstr[:4]
elif len(dstr) < 4:
    dstr = "%4s" % dstr

ser = serial.Serial('/dev/ttyACM0')
ser.write(bytearray('%s\n' % dstr, 'utf-8'))
ser.close()
