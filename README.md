Quickstart:
# sudo apt-get install portaudio19-dev
# sudo pip3 install pyaudio
# sudo pip3 install obd
# python3 /path/to/Maxine.py

This is a project designed to handle all the things I would like to add to the Raspberry Pi in my vehicle.

It will include OBD inputs to generate sound in real time, custom security, sound fx for various events, theme music for events, smart ass backseat driver comments for GPS, and so much more.

Using https://github.com/brendan-w/python-OBD.git for the OBD backend, 'cause it rocks (async data polling ftw).

Currently there isn't much. This is really just to tie in my dev area on the Pi itself to the corresponding git repo.

Ideas in the works:
 - General engine fault warnings
 - General engine data displays/reporting
 - Webcam motion detection while vehicle is off
   - Accessible via network, if connected
   - Late night warnings via push/sms notification
 - Connect to known APs automatically
   - If no known AP found, become one
 - Generate synthetic sound effects based on engine data, output to stereo
 - Media capabilities, I suppose. People love their media.
 - Additional sensor data via GPIO
   - Door switches
   - Tilt sensor
 - Scan for bugged fuel pumps and issue warning if found
   - Going to be based on https://github.com/sparkfunX/Skimmer_Scanner

Stay tuned! Or don't, I don't care. This is for me.

Licensing: I haven't picked one yet, so for now it's a generic 'Do what you want, but do not blame me. I told you not to.'
