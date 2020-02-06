### StatusIndicator

Uses a 4-digit, 14-segment LED display to indicate out-of-office status, updated
automatically through a Google calendar.  Calendar interface adapted from
[Google API quickstart](https://developers.google.com/calendar/quickstart/python).
Use this to set up credentials.json file.  Calendar should contain events with
4-character (or less) names.

##### Hardware
+   [Adafruit ItsyBitsy 32u4 - 5V 16MHz](https://www.adafruit.com/product/3677)
+   [Adafruit Quad Alphanumeric Display](https://www.adafruit.com/product/1912)

##### Library Dependencies
+   [Adafruit LED Backpack](https://github.com/adafruit/Adafruit_LED_Backpack)
+   [Google API Client](https://developers.google.com/api-client-library/python/)
+   [PySerial](https://pythonhosted.org/pyserial/)

##### Installation
1.  Clone repository
2.  Create and activate virtualenv
3.  Install requirements
4.  Get credentials.json file from Google APIs
5.  Create config file from template, check authentication
6.  Update systemd files to point to install location
7.  Copy/symlink systemd files to systemd directory
8.  Enable/start timer
