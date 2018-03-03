#!/bin/bash

#dat=$(grep -Ev "^Time" /dev/shm/jeep_obd.log | sed -e '1{$d;}' -e '$!{h;d;}' -e x | sed 's/NODATA/--/g')
dat=$(tail -1 /dev/shm/obdstat.dat)

# put all data into 'data' array
# timestamp, rpm, tps, coolant temp, mph
IFS=',' read -r -a data <<< "$dat"

echo "\${font mono:size=18}${data[2]}MPH  \$alignc ${data[3]}RPM  \$alignr Temp: ${data[5]}"
echo "\${font mono:size=14}Voltage: ${data[6]} \$alignc Fuel: ${data[7]} \$alignr Throttle: ${data[4]}"
