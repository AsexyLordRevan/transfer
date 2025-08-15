#!/bin/su root

source=~/.zshrc
cd ~/.config/colours
choices=$(python pysync.py)
chosen=$(printf  \
    | rofi -theme-str '@import "config.rasi"' \
           -dmenu \
           -sep ';' \
           -selected-row 2 -config ~/.config/rofi/script.rasi)

case "$chosen" in
    "$power_off  Power Off")
        bash ~/.config/rofi/apps/prompt.sh --query 'Shutdown?' && poweroff
        ;;

    "$reboot  Reboot")
        bash ~/.config/rofi/apps/prompt.sh --query 'Reboot?' && reboot
        ;;

    "$lock  Lock Screen")
        hyprlock
        ;;

    "$throttle  Throttle Off")
        sudo systemctl start t2fanrd
        ;;

    "$log_out  Log Out")
	killall Hyprland
        ;;
    "Fan On")
	sudo systemctl start t2fanrd
	;;
    *) exit 1 ;;
esac
