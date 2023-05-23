#!/bin/bash

FILE=$PWD/marktplatz.db

if ! test -f "$FILE"; then
    echo "$FILE does not exist: executing initial database build"
    python $PWD/scripts/first_build.py
    sleep 2

fi

while true
do
	echo "$(date +"%T"): Updating every 10m"
  python $PWD/scripts/updater.py
	sleep 600
done