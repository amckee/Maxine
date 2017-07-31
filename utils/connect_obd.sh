#!/bin/bash

sudo rfcomm connect 0 00:1D:A5:00:01:EB & >> /dev/shm/maxine.log
(sleep 2s && sudo rfcomm bind 0 00:1D:A5:00:01:EB) >> /dev/shm/maxine.log
sleep 1


