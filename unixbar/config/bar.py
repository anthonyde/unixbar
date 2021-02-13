"""
Bar configuration
"""

import collections
import subprocess

from ..bin import environ as bin_environ
from ..lib import lemonbar

from . import chars
from . import colors
from . import util

__all__ = [
  "BAR_ZWSP",
  "bar_args",
  "bar_click",
  "print_bar"
  ]

BAR_ZWSP = chars.ZWSP

BAR_PAD_HEIGHT = 23
BAR_BORDER_WIDTH = 4

BAR_HEIGHT = BAR_PAD_HEIGHT + BAR_BORDER_WIDTH

BAR_FONTS = (
  "Helvetica Neue:pixelsize=13",
  "Helvetica Neue:style=Bold Italic:pixelsize=13", # Title
  "Helvetica Neue:pixelsize=12", # Battery percentage
  "FreeSans:style=Bold:pixelsize=16", # MULT, ZWSP
  "i3fonticon:pixelsize=16",
  "IcoMoon\-Free:pixelsize=16",
  "i3fonticon:pixelsize=10:matrix=0 -1.49 1.17 0" # Battery (vertical)
  )

def bar_args():
  """Return the bar command with arguments."""
  # This configuration requires a version of lemonbar with Xft and foreground
  # transparency support.  See https://github.com/anthonyde/bar for a
  # compatible version.
  return lemonbar.bar_args(
    "lemonbar",
    geometry=(None, BAR_HEIGHT, None, None),
    fonts=BAR_FONTS,
    underline=2,
    bg=colors.background,
    fg=colors.foreground,
    offset=BAR_BORDER_WIDTH // -2
    )

def bar_click(k, v):
  """Do something when the bar is clicked."""
  if k == "audio":
    subprocess.Popen(["alacritty", "-e", "alsamixer"])
  elif k == "bat":
    subprocess.Popen(["gnome-power-statistics"])
  elif k == "clip":
    subprocess.Popen(["clipboard-clear"], env=bin_environ())
  elif k == "mpd":
    subprocess.Popen(["ffplay", "-autoexit", "http://mpd:8001/mpd.flac"])
  elif k == "red":
    subprocess.Popen(["killall", "-USR1", "redshift"])
  elif k == "wifi":
    subprocess.Popen(["wpa_gui"])

LEFT_FMT = "%{{l}}{pad}{v[tags]}%{{c}}{v[title]}"
RIGHT_VIEWS = ["clip", "red", "mpd", "vpn", "wifi", "audio", "bat", "clock"]

def print_bar(**views):
  """Print the bar contents."""
  nonempty_views = util.nonempty_keys(views)
  right_fmt = "%{{r}}" + "{sep}".join(
    "{{v[{}]}}".format(v) for v in RIGHT_VIEWS if v in nonempty_views
    ) + "{pad}"
  print((LEFT_FMT + right_fmt).format(
      c=colors,
      v=collections.ChainMap(views, collections.defaultdict(str)),
      pad=chars.ENSP,
      sep=chars.EMSP
      ))
