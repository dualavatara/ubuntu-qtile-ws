from libqtile.config import Key, Screen, Group, Drag, Click, Match, Rule
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook
from libqtile.manager import Qtile
from itertools import cycle
import pprint
import sys
import logging
import re

mod = "mod4"
alt = "mod1"

keys = [
    # Switch between windows in current stack pane
    Key(
        [mod], "k",
        lazy.layout.down()
    ),
    Key(
        [mod], "j",
        lazy.layout.up()
    ),

    # Move windows up or down in current stack
    Key(
        [mod, "control"], "k",
        lazy.layout.shuffle_down()
    ),
    Key(
        [mod, "control"], "j",
        lazy.layout.shuffle_up()
    ),

    # Switch window focus to other pane(s) of stack
    Key(
        [mod], "space",
        lazy.layout.next()
    ),

    # Swap panes of split stack
    Key(
        [mod, "shift"], "space",
        lazy.layout.rotate()
    ),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"], "Return",
        lazy.layout.toggle_split()
    ),
    Key([mod], "Return", lazy.spawn("xterm")),

    #sound control soecial keys
    Key([], "XF86AudioMute", lazy.spawn("amixer sset Master playback 0%")),
    Key([], "XF86AudioLowerVolume", lazy.spawn("amixer sset Master playback 5dB-")),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("amixer sset Master playback 5dB+")),

    # program launchers
    Key([mod, "shift"], "e", lazy.spawn("~/eve.sh")),
    Key([mod, "shift"], "p", lazy.spawn("pycharm")),
    Key([mod, "shift"], "g", lazy.spawn("google-chrome")),
    Key([mod, "shift"], "m", lazy.spawn("mine")),
    Key([mod], "l", lazy.spawn("gnome-screensaver-command -l")),

    # Toggle between different layouts as defined below
    # Key([mod], "Tab", lazy.switchgroup()),
    Key([mod, "control"], "Tab", lazy.nextlayout()),
    Key([mod], "w", lazy.window.kill()),

    Key(
        [mod], "F12",
        lazy.window.toggle_fullscreen()
    ),

    # maximize and minimize
    Key([mod], "m", lazy.window.toggle_maximize()),
    Key([mod], "n", lazy.window.toggle_minimize()),

    Key([mod, "control"], "r", lazy.restart()),
    Key([mod, "control"], "q", lazy.shutdown()),
    Key([mod], "r", lazy.spawncmd()),
]

groups = [
    Group(
        "term",
        matches=[
            Match(wm_class=["XTerm"])
        ],
        exclusive=True,
        layout="stack",
        position=1,
        screen_affinity=1
    ),
    Group(
        "dev",
        matches=[
            Match(wm_class=[re.compile("jetbrains.*", re.IGNORECASE)])
        ],
        position=2,
        screen_affinity=0
    ),
    Group(
        "web",
        matches=[
            Match(role=['browser', 'GtkFileChooserDialog']),
        ],
        position=3,
        exclusive=False
    ),
    Group(
        "task",
        matches=[
            Match(wm_instance_class=[
                re.compile(".*pivot.*", re.IGNORECASE),
                re.compile(".*in-sight.*", re.IGNORECASE),
                re.compile(".*slack\\.com.*", re.IGNORECASE),
            ]),
            Match(role=['GtkFileChooserDialog']),
            Match(wm_class=['Skype'])
        ],
        layout="max",
        position=4
    ),
    Group("mail",
          matches=[
              Match(wm_instance_class=[re.compile("mail.google.com.*", re.IGNORECASE)]),
              Match(role=['GtkFileChooserDialog']),
          ],
          position=5
    ),
    Group("other",
          matches=[
              Match(wm_class=[re.compile(".*", re.IGNORECASE)])
          ],
          position=6
    )
]

idx = 0
gkeys = "1234567890"
for grp in groups:
    # # mod1 + letter of group = switch to group
    keys.append(
        Key([mod], gkeys[idx], lazy.group[grp.name].toscreen())
    )

    # mod1 + shift + letter of group = switch to & move focused window to group
    keys.append(
        Key([mod, "shift"], gkeys[idx], lazy.window.togroup(grp.name))
    )
    idx += 1

# groups = [Group(i) for i in "asdfuiop"]
#
# for i in groups:
# # mod1 + letter of group = switch to group
# keys.append(
# Key([mod], i.name, lazy.group[i.name].toscreen())
#     )
#
#     # mod1 + shift + letter of group = switch to & move focused window to group
#     keys.append(
#         Key([mod, "shift"], i.name, lazy.window.togroup(i.name))
#     )

layouts = [
    layout.Max(),
    layout.Stack(num_stacks=2)
]

widget_defaults = dict(
    font='Arial',
    fontsize=16,
    padding=3,
)

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(),
                widget.Prompt(),
                widget.WindowName(),
                widget.CurrentLayout(),
                widget.CPUGraph(line_width=1, width=50, graph_color='00ff00'),
                widget.MemoryGraph(line_width=1, width=50, graph_color='0000ff'),
                widget.HDDBusyGraph(line_width=1, width=50, graph_color='ffff00'),
                widget.Battery(format='{percent:1.0%}'),
                widget.Wlan(interface='wlan0'),
                widget.Systray(),
                widget.KeyboardLayout(configured_keyboards=['us', 'ru']),
                widget.Clock(),
            ],
            30,
        ),
    ),
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(),
                widget.Prompt(),
                widget.WindowName(),
                widget.CurrentLayout()
            ],
            30,
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
dgroups_app_rules = []
main = None
follow_mouse_focus = False
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating()
auto_fullscreen = False
wmname = "LG3D"


@hook.subscribe.startup
def runner():
    import subprocess

    """
    Run after qtile is started
    """


    # startup-script is simple a list of programs to run
    #subprocess.Popen('/home/dualavatara/qtile_startup.sh')
    subprocess.Popen(['wicd-client', '-t'])
    subprocess.Popen('google-chrome', shell=True)


@hook.subscribe.client_new
def dialogs(window):
    if (window.window.get_wm_type() == 'dialog'
        or window.window.get_wm_transient_for()):
        window.floating = True


@hook.subscribe.client_new
def vue_tools(window):
    if ((window.window.get_wm_class() == ('sun-awt-X11-XWindowPeer',
                                          'tufts-vue-VUE', 'wicd-client.py', 'Wicd-client.py')
         and window.window.get_wm_hints()['window_group'] != 0)
        or (window.window.get_wm_class() == ('sun-awt-X11-XDialogPeer',
                                             'tufts-vue-VUE'))):
        window.floating = True


@hook.subscribe.client_new
def idle_dialogues(window):
    if ((window.window.get_name() == 'Search Dialog') or
            (window.window.get_name() == 'Module') or
            (window.window.get_name() == 'Goto') or
            (window.window.get_name() == 'IDLE Preferences')):
        window.floating = True


@hook.subscribe.client_new
def libreoffice_dialogues(window):
    if ((window.window.get_wm_class() == ('VCLSalFrame', 'libreoffice-calc')) or
            (window.window.get_wm_class() == ('VCLSalFrame', 'LibreOffice 3.4'))):
        window.floating = True
    if (window.window.get_wm_class() == ('wicd-client.py', 'Wicd-client.py')):
        #window.enablefloating()
        #window.tweak_float()
        hints = window.window.get_wm_normal_hints()
        nw = hints['min_width'];
        nh = hints['min_height'];
        screen = window.qtile.find_closest_screen(0, 0)
        nx = (screen.width - nw) / 2
        ny = (screen.height - nh) / 2
        window._enablefloating(x=nx, y=ny, w=nw, h=nh)


@hook.subscribe.client_new
def inkscape_dialogues(window):
    if (window.window.get_name() == 'Sozi'):
        window.floating = True


@hook.subscribe.client_new
def inkscape_dialogues(window):
    if ((window.window.get_name() == 'Create new database')):
        window.floating = True
