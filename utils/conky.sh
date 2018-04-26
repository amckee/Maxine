#!/bin/bash

dat=$(tail -1 /dev/shm/obdstat.dat)

# put all data into 'data' array
# csv values are:
# timestamp,mph,rpm,tps,temp,volt,fuel
IFS=',' read -r -a data <<< "$dat"

echo "\${font mono:size=18}${data[2]}MPH  \$alignc ${data[3]}RPM  \$alignr Temp: ${data[5]}"
echo "\${font mono:size=14}Voltage: ${data[6]} \$alignc Fuel: ${data[7]} \$alignr Throttle: ${data[4]}"
