"""
Color definitions
"""

import re

from . import xrdb

__all__ = []

# General
background = "#00000000"
foreground = xrdb.foreground
underline = xrdb.color12

# Battery
bat_warn = xrdb.color11
bat_crit = xrdb.color9

# herbstluftwm
herbst_tag_empty = re.sub(r"^#..", "#80", xrdb.foreground)

# OSD
osd_background = "#11ffffff"
osd_foreground = "#ee000000"