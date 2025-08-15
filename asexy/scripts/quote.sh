#!/bin/bash
/usr/bin/jq -r 'to_entries | .[] | "\(.key) — \(.value)"' /home/revan/.config/asexy/configs/quotes.json | /usr/bin/shuf -n 1
