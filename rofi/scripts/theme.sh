#!/bin/bash
cd ~
chosen=$(printf '%s;%s;%s;%s;%s;%s\n' "Screenshot" "Colour Picker" "Colour Select" "Theme Select" "Wallpaper Select"\
    | rofi -dmenu -config ~/.config/rofi/script.rasi -sep ';')

case "$chosen" in
    "Screenshot")
        grim -g "$(slurp -d)" - | wl-copy
        ;;

    "Colour Select")
        python /home/revan/.config/colours/pysync.py -crl
        ;;

    "Colour Picker")
        hyprpicker
        ;;

    "Save Theme")
        python /home/revan/.config/colours/pysync.py -sr
        ;;

    "Theme Select")
	    
        python /home/revan/.config/colours/pysync.py -tr
        ;;
    "Wallpaper Select")
	    python /home/revan/.config/colours/pysync.py -wr
	    ;;
    *) exit 1 ;;
esac
