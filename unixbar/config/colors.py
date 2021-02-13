"""
Color definitions
"""

import re

from . import xrdb

__all__ = []

# General
background = "#00000000"
foreground = xrdb.foreground
active = xrdb.color13
warning = xrdb.color11

# Battery
bat_warn = warning
bat_crit = xrdb.color9

# herbstluftwm
herbst_tag_empty = re.sub(r"^#..", "#80", xrdb.foreground)
herbst_tag_focused = active
herbst_tag_urgent = warning

# OSD
osd_background = "#11ffffff"
osd_foreground = "#ff000000"
