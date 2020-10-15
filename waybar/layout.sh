#/bin/sh
swaymsg -rt get_inputs | sed -nE 's/.*"xkb_active_layout_index":[[:blank:]]*([0-9]*).*/\1/p'|sed 's/0/🇺🇸 us/; s/1/🇷🇺 ru/; q'
