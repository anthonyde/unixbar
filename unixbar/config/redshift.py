"""
Configuration for a redshift status icon and OSD
"""

from .. import data
from .. import util
from .. import view

__all__ = []

# redshift symbols (i3fonticon)
RED_OFF = "\ue81a"
RED_ON = "\ue819"

@data.transformer(keys=["red_stat"])
@data.on_val(key="red_on")
def transform_to_bool(v):
  """Transform "Enabled"/other -> True/False."""
  return "Enabled" == v

@view.viewer
@util.staticvars(_first=True)
def view_red(osd_out, red_on=False, **ds):
  """View the redshift status on the bar and changes in an OSD."""
  sym = RED_ON if red_on else RED_OFF

  if not view_red._first:
    print("%{{c}}{sym}\n".format(sym=sym), file=osd_out)
  print("red=%{{A:red:}}{sym}%{{A}}".format(sym=sym))

  view_red._first = False
