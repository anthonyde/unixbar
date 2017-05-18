"""
Configuration for a backlight OSD
"""
import os

from .. import data
from .. import view

from . import util

__all__ = []

os.environ["BL_DEV"] = "intel_backlight"

BL_SYM = "\ue8af" # i3fonticon

BL_N_MAX = 16

@data.transformer(keys=["bl_bness", "bl_bness_max", "bl_power"])
@data.on_val()
def transform_to_int(v):
  """Transform a string to an int."""
  return int(v)

@view.viewer
@util.staticvars(_first=True, _last_power=0)
def view_bl(osd_out, bl_bness=0, bl_bness_max=0, bl_power=0, **ds):
  """View backlight changes in an OSD."""
  if not view_bl._first and view_bl._last_power == bl_power:
    print("%{{c}}{sym}\n%{{c}}%{{T2}}{bness_bar}%{{T-}}".format(
        sym=BL_SYM,
        bness_bar=util.prog_bar(bl_bness * BL_N_MAX // bl_bness_max, BL_N_MAX)
        ),
      file=osd_out
      )

  view_bl._first = False
  view_bl._last_power = bl_power
