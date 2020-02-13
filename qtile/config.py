# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import os
import subprocess
from libqtile.config import Key, Screen, Group, Drag, Click
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook
from layouts import layouts, floating_layout
from colors import colors


from typing import List  # noqa: F401

#some variables 
vol_curr      = "amixer -D pulse get Master"
vol_up       = "amixer -q -D pulse sset Master 2%+"
vol_down     = "amixer -q -D pulse sset Master 2%-"
mute         = "amixer -q -D pulse set Master toggle"
bright_up   = "light -A 5"
bright_down = "light -U 5"
mod = "mod4"
separator = {'linewidth': 2, 'size_percent': 70,
        'foreground': 'F3F3F3', 'padding': 7}

keys = [
    #Volume/Brightness
    Key([], "XF86AudioRaiseVolume", lazy.spawn(vol_up)),
    Key([], "XF86AudioLowerVolume", lazy.spawn(vol_down)),
    Key([], "XF86AudioMute", lazy.spawn(mute)),
    Key([], "XF86MonBrightnessUp", lazy.spawn(bright_up)),
    Key([], "XF86MonBrightnessDown", lazy.spawn(bright_down)),
    # Switch between windows in current stack pane
    Key([mod], "k", lazy.layout.down()),
    Key([mod], "j", lazy.layout.up()),

    # Move windows up or down in current stack
    Key([mod, "control"], "k", lazy.layout.shuffle_down()),
    Key([mod, "control"], "j", lazy.layout.shuffle_up()),

    # Switch window focus to other pane(s) of stack
    Key([mod], "space", lazy.layout.next()),

    # Swap panes of split stack
    Key([mod, "shift"], "space", lazy.layout.rotate()),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "Return", lazy.layout.toggle_split()),
    Key([mod], "Return", lazy.spawn("kitty")),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout()),
    Key([mod], "w", lazy.window.kill()),

    Key([mod, "control"], "r", lazy.restart()),
    Key([mod, "control"], "q", lazy.shutdown()),
    Key([mod], "r", lazy.spawncmd()),
]

groups = [Group(i) for i in "12345678"]

for i in groups:
    keys.extend([
        # mod1 + letter of group = switch to group
        Key([mod], i.name, lazy.group[i.name].toscreen()),

        # mod1 + shift + letter of group = switch to & move focused window to group
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name)),
    ])


widget_defaults = dict(
    font='Noto Sans',
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()

#font awesome icons v4.7
icons = { "brightness" : "",
         "battery" : "",
         "volume" : "",
         "wlan" : "",
         "weather" : ""
        }
style = { "fg" : colors["greybg"],
        }


screens = [
    Screen(
        bottom=bar.Bar(
            [
                widget.GroupBox(
                    other_current_screen_border=colors["red_1"],
                    this_current_screen_border=colors["greybg"],
                    other_screen_border=colors["red_1"],
                    this_screen_border=colors["black"],
                    highlight_color=colors["greyfg"],
                    urgent_border=colors["red_1"],
                    background=colors["greyfg"],
                    highlight_method="line",
                    inactive=colors["white"],
                    active=colors["black"],
                    disable_drag=True,
                    borderwidth=5),
                widget.TextBox(font="Arial", foreground=colors["greyfg"], text="► ", fontsize=38,padding=-6),
                widget.Prompt(bell_style="visual"),
                widget.WindowName(),
                #widget.TextBox(text=icons["weather"],background=colors["greyfg"],  **style),
                #widget.YahooWeather(woeid="834463",format="{condition_temp} °{units_temperature}",background=colors["greyfg"],  **style),
                widget.TextBox(font="Arial", foreground=colors["greyfg"], text="◄", fontsize=38,padding=-6),
                widget.TextBox(text=icons["wlan"],background=colors["greyfg"],foreground=colors["greybg"],  **style),
                widget.Wlan(interface="wlo1",disconnected_message="Disconnected",format="{essid} {percent:2.0%}",background=colors["greyfg"],foreground=colors["greybg"]),
                widget.TextBox(text=icons["brightness"],background=colors["greyfg"],foreground=colors["greybg"],  **style),
                widget.Backlight(
                    backlight_name="amdgpu_bl0",background=colors["greyfg"],foreground=colors["greybg"],  **style),
                widget.TextBox(text=icons["volume"],background=colors["greyfg"],foreground=colors["greybg"],  **style),
                widget.Volume(get_volume_command=vol_curr.split(),background=colors["greyfg"],foreground=colors["greybg"],  **style),
                widget.TextBox(text=icons["battery"],background=colors["greyfg"],foreground=colors["greybg"],  **style),
                widget.Battery(format="{percent:.0%}",background=colors["greyfg"],foreground=colors["greybg"], **style),
                widget.Systray(),
                widget.Clock(timezone="Europe/Minsk", format='%Y-%m-%d %a %I:%M %p',background=colors["greyfg"],foreground=colors["greybg"], **style),
            ],
            24, background=colors["greybg"]
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
#main = None
follow_mouse_focus = True
bring_front_click = True
cursor_warp = False
auto_fullscreen = True
focus_on_window_activation = "smart"

# Startup file

@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.call([home])



# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
