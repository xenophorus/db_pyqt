#!/bin/bash

konsole -e ./server.py -d 127.0.0.1 -p 9000 &
sleep 1
konsole -e ./client.py -d 127.0.0.1 -p 9000 -n alex &
sleep 1
konsole -e ./client.py -d 127.0.0.1 -p 9000 -n john &
sleep 1
konsole -e ./client.py -d 127.0.0.1 -p 9000 -n ann &
sleep 1
konsole -e ./client.py -d 127.0.0.1 -p 9000 -n helen &
sleep 1
konsole -e ./client.py -d 127.0.0.1 -p 9000 -n aida &
sleep 1
konsole -e ./monitor.py

