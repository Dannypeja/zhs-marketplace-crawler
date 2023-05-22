#!/bin/bash

FILE=$PWD/marktplatz.db

if ! test -f "$FILE"; then
    echo "$FILE does not exist: executing initial database build"
    python $PWD/scripts/first_build.py
    sleep 2

fi

while true
do
	echo "Looking for Database Update every 10 minutes: Press ctrl+C to exit or kill container"
  python $PWD/scripts/updater.py
	sleep 600
done