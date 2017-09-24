#!/bin/bash

## manage connections to OBD ( 00:1D:A5:00:01:EB )

disconnect(){
  sudo rfcomm disconnect 0 >> /dev/shm/maxine.log
  sudo rfcomm unbind 0 >> /dev/shm/maxine.log
  sleep 1
}

connect(){
  sudo rfcomm connect 0 00:1D:A5:00:01:EB & >> /dev/shm/maxine.log
  (sleep 2s && sudo rfcomm bind 0 00:1D:A5:00:01:EB) >> /dev/shm/maxine.log
  sleep 1
}

connected(){
  return hcitool con | grep -q '00:1D:A5:00:01:EB'
}

main(){
  if connected; then
    disconnect
  fi
  connect
}

main
