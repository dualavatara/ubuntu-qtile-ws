#!/bin/bash

xrandr | grep VGA | grep " connected "
if [ $? = "0" ]; then
    # External monitor is connected
    xrandr --output VGA1 --mode 1920x1200 --primary --rate 60.0 --output LVDS1 --mode 1366x768 --rate 60.0 --left-of VGA1
    if [ $? != 0 ]; then
        # Something went wrong. Autoconfigure the internal monitor and disable the external one
        xrandr --output LVDS1 --mode auto --output VGA1 --off
    fi
else
    # External monitor is not connected
    xrandr --output LVDS1 --mode 1366x768 --output VGA1 --off
fi
