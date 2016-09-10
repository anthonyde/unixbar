"""
A library exporting xdotool functionality
"""

from .. import subprocessx as subprocess

def dpy_size():
  """Get the display width and height."""
  geom_str = subprocess.check_output_text(["xdotool", "getdisplaygeometry"])
  w, h = geom_str.split()
  return int(w), int(h)
