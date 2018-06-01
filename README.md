Quickstart:
- apt-get install portaudio19-dev
- pip3 install pyaudio
- pip3 install obd
- pip3 install pybluez
- python3 /path/to/Maxine.py
- sudo ln -s /path/to/Maxine/etc/logrotate /etc/logrotate.d/maxine

This is a project designed to handle all the things I would like to add to the Raspberry Pi in my vehicle.

It will include OBD inputs to generate sound in real time, custom security, sound fx for various events, theme music for events, smart ass backseat driver comments for GPS, and so much more.

Using https://github.com/brendan-w/python-OBD.git for the OBD backend, 'cause it rocks (async data polling ftw).

Currently there isn't much. This is really just to tie in my dev area on the Pi itself to the corresponding git repo.
Working:
 - Fan controlled based on CPU temperature to reduce power usage
 - Auto scan, find and connect to OBD bluetooth device
 - OBD data pulling, with output to file for external tool usage

TODO:
 - General engine fault warnings
 - General engine data displays/reporting
 - Webcam motion detection while vehicle is off
   - Accessible via network, if connected
   - Event warnings via push/sms notification
 - Connect to known APs automatically
   - If no known AP found, become one
 - Generate synthetic sound effects based on engine data, output to stereo
 - Media capabilities, I suppose. People love their media.
 - Additional sensor data via GPIO
   - Door switches
     - Event warnings via push/sms
   - Tilt sensor
 - Scan for bugged fuel pumps and issue warning if found
   - Going to be based on https://github.com/sparkfunX/Skimmer_Scanner
 - Wise cracking GPS
 - AI based backseat driver
 - Sound FX for various driving events
   - Hit brakes, play https://www.youtube.com/watch?v=6OjUE5FAN0E
   - Hit gas, play https://www.youtube.com/watch?v=NahjHrIHp20
   - Hit wall, play https://www.youtube.com/watch?v=5CsyGe4F8CQ

Stay tuned! Or don't, I don't care. This is for me.

Licensing: I haven't picked one yet, so for now it's a generic 'Do what you want, but do not blame me. I told you not to.'
