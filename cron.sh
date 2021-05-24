#!/bin/bash

echo "Running spiders at 11:00 and 23:00 local time..."

while :
do
	  startTime=$(date +%s)
	  endTime0=$(date -d "tomorrow 11:00" +%s)
	  endTime1=$(date -d "tomorrow 23:00" +%s)
	  timeToWait=$(($endTime0- $startTime))
	  /bin/sleep $timeToWait

	  python manage.py crawl

	  startTime=$(date +%s)
	  timeToWait=$(($endTime1- $startTime))
	  /bin/sleep $timeToWait

	  python manage.py crawl
done
