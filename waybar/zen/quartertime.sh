#!/bin/bash

# Get current hour and minute
hour=$(date +%H)
minute=$(date +%M)

# Round minute to nearest 15
rounded_minute=$(( ( (10#$minute + 7) / 15 ) * 15 ))
if [ "$rounded_minute" -eq 60 ]; then
  rounded_minute=0
  hour=$(( (10#$hour + 1) % 24 ))
fi

# Format with leading zeros
printf "%02d:%02d\n" $hour $rounded_minute
