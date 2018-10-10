StatusIndicator

Uses a 4-digit, 14-segment LED display to indicate out-of-office status, updated
automatically through a Google calendar.  Calendar interface adapted from
https://developers.google.com/calendar/quickstart/python.  Use this to set
up credentials.json file.

Hardware:
https://www.adafruit.com/product/3677
https://www.adafruit.com/product/1912

Library Dependencies:
https://github.com/adafruit/Adafruit_LED_Backpack
https://developers.google.com/api-client-library/python/
https://pythonhosted.org/pyserial/

Installation:
1. Clone repository
2. Create and activate virtualenv
3. Install requirements
4. Get credentials.json file from Google APIs
5. Create config file from template, check authentication
6. Update systemd files to point to install location
7. Copy/symlink systemd files to systemd directory
8. Enable/start timer
