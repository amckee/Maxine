#!/bin/bash

if [ ! -f /dev/shm/maxine.log ]; then
	touch /dev/shm/maxine.log
fi
if [ ! -f /dev/shm/obdstat.log ]; then
	touch /dev/shm/obdstat.log
fi

conky -c /home/pi/bin/Maxine/utils/conky.rc
