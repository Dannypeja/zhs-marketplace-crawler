#!/bin/bash

FILE=$PWD/marktplatz.db

if ! test -f "$FILE"; then
    echo "$FILE does not exist: executing initial database build"
    python $PWD/scripts/first_build.py
    sleep 2

fi

while true
do
	echo "\n looking for Database Update every 15 seconds: Press ctrl+C to exit or kill container \n"
  python $PWD/scripts/updater.py
	sleep 15
done