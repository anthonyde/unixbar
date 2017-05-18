"""
Configuration for OSD appearance and behavior
"""

from .. import util
from ..lib import lemonbar
from ..lib import xdotool

from . import colors

OSD_DELAY_MS = 2500

OSD_DEFAULT_ARGS = dict(
  w=200,
  name="osd",
  bg=colors.osd_background,
  fg=colors.osd_foreground
  )

OSD_BAR_ARGS = [
  dict(
    h=150,
    fonts=(
      "Helvetica Neue:pixelsize=100",
      "i3fonticon:pixelsize=99", # 100 causes incorrect width for some glyphs
      "IcoMoon\-Free:pixelsize=100"
      )
    ),
  dict(
    h=40,
    fonts=(
      "Helvetica Neue:pixelsize=13", # WiFi name
      "DejaVu Sans:pixelsize=9" # Volume bar
      )
    )
  ]

@util.compose(list)
def osd_argss():
  """Return OSD commands with arguments, one set per panel."""
  # Sorry, Guido
  argss = [dict(OSD_DEFAULT_ARGS, **args) for args in OSD_BAR_ARGS]
  dw, dh = xdotool.dpy_size()
  hsum = sum(args["h"] for args in argss)
  y = (dh - hsum) * 4 // 5
  for args in argss:
    w = args.pop("w")
    h = args.pop("h")
    x = (dw - w) // 2
    args["geometry"] = (w, h, x, y)
    yield lemonbar.bar_args("lemonbar", **args)
    y += h
