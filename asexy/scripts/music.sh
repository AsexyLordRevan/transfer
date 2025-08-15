#!/bin/bash

last_status=""

while true; do
  status=$(playerctl status 2>/dev/null)

  # Default if nothing is playing or error
  if [[ -z "$status" ]]; then
    status="Unknown"
  fi

  # Only print if status changed
  if [[ "$status" != "$last_status" ]]; then
    echo "{\"class\": \"$status\"}"
    last_status="$status"
  fi

  sleep 0.5
done
