#!/bin/su root

source=~/.zshrc
power_off=''
reboot=''
lock=''
throttle=' '
log_out='󰗽 '

chosen=$(printf '%s;%s;%s;%s;%s\n' "$power_off  Power Off" "$reboot  Reboot" "$lock  Lock Screen" "$log_out  Log Out" \
    | rofi  -config ~/.config/rofi/script.rasi \
           -dmenu \
           -sep ';' \
           -selected-row 2)

case "$chosen" in
    "$power_off  Power Off")
        bash ~/.config/rofi/scripts/prompt.sh --query 'Shutdown?' && poweroff
        ;;

    "$reboot  Reboot")
        bash ~/.config/rofi/scripts/prompt.sh --query 'Reboot?' && reboot
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
