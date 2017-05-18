"""
Configuration for a keyboard status icon
"""

from .. import data
from .. import view

__all__ = []

# Keyboard symbols (IcoMoon-Free)
KB_DEFAULT = "\ue955"
KB_NUMLOCK = "\ue940"

@data.transformer(keys=["kb_leds"])
@data.on_val(key="kb_numlock")
def transform_to_numlock(v):
  """Transform a keyboard LED mask to a Num Lock flag."""
  return int(v) & 2 != 0

@view.viewer
def view_kb(kb_numlock=None, **ds):
  """View the keyboard status on the bar."""
  print("kb=%{{T6}}{sym}%{{T-}}".format(
    sym=KB_NUMLOCK if kb_numlock else KB_DEFAULT
    ))
