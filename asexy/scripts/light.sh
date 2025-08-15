#!/bin/bash

last_brightness=""

while true; do

  # Calculate percentage
  brightness=$(brightnessctl -d acpi_video0 g)

  # Determine class
  if (( brightness <= 39 )); then
    class="lowest"
  elif (( brightness <= 59 )); then
    class="low"
  elif (( brightness <= 79 )); then
    class="medium"
  elif (( brightness <= 99 )); then
    class="high"
  else
    class="highest"
  fi


# Only print if brightness changed
if [[ "$brightness" != "$last_brightness" ]]; then
  echo "{\"percentage\": $brightness, \"class\": \"$class\"}"
  last_brightness="$brightness"
fi

  sleep 0.5
done
