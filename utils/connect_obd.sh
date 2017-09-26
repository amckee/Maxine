#!/bin/bash

main(){
        sudo hcitool cc 00:1D:A5:00:01:EB
        sudo rfcomm bind 0 00:1D:A5:00:01:EB
}

main
