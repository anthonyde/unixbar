"""
Configuration for battery status information and notifications
"""

import os

from .. import data
from .. import util
from .. import view
from ..lib import notify

from . import chars
from . import colors

__all__ = []

os.environ["BAT_DEV"] = "BAT0"

# Warning states
BAT_CAP_NOTIFY = 10
BAT_CAP_CRIT = 13
BAT_CAP_WARN = 20

# Capacity symbols (i3fonticon)
BAT_ZERO = "\uec0f"
BAT_QRTR = "\uec0e"
BAT_HALF = "\uec0d"
BAT_3QTR = "\uec0c"
BAT_FULL = "\uec0b"

# Capacity states
BAT_CAP_ZERO = 13
BAT_CAP_QRTR = 38
BAT_CAP_HALF = 63
BAT_CAP_3QTR = 88

# Status symbols
BAT_STAT_UNKNOWN = chars.MULT
BAT_STAT_CHARGE = "\ue8d8" # i3fonticon

def bat_notify(cap, stat):
  """Return whether this status requires notification."""
  return cap is not None and cap < BAT_CAP_NOTIFY and stat != "Charging"

def bat_color(cap):
  """Return the color string for a capacity."""
  if cap is not None:
    if cap < BAT_CAP_CRIT:
      return colors.bat_crit
    elif cap < BAT_CAP_WARN:
      return colors.bat_warn
  return "-"

def bat_sym(cap):
  """Return the symbol for a capacity."""
  if cap is None or cap < BAT_CAP_ZERO:
    return BAT_ZERO
  elif cap < BAT_CAP_QRTR:
    return BAT_QRTR
  elif cap < BAT_CAP_HALF:
    return BAT_HALF
  elif cap < BAT_CAP_3QTR:
    return BAT_3QTR
  else:
    return BAT_FULL

@data.transformer(keys=["bat_cap"])
@data.on_val()
def transform_to_int(v):
  """Transform a string to an int."""
  return int(v)

@data.transformer(keys=["blink"])
@data.on_val()
def transform_to_bool(v):
  """Transform non-zero/zero -> True/False."""
  return bool(int(v))

@view.viewer
@util.staticvars(_last_notify=False, _note=notify.Note(body="Plug it in"))
def view_bat(blink_listeners, blink=False, bat_cap=None, bat_stat=None, **ds):
  """View the battery status on the bar and notify when it's low."""
  color = bat_color(bat_cap)
  notify_ = bat_notify(bat_cap, bat_stat)

  stat_sym = None
  if bat_stat == "Charging":
    stat_sym = BAT_STAT_CHARGE
  elif bat_stat == "Discharging" and notify_ and blink:
    color = "-"
  elif bat_stat is None:
    stat_sym = BAT_STAT_UNKNOWN

  if notify_:
    blink_listeners.add(view_bat)
  else:
    blink_listeners.discard(view_bat)

  if notify_:
    view_bat._note.summary = "Low battery ({cap}%)".format(cap=bat_cap)
    view_bat._note.update()

  if notify_ and not view_bat._last_notify:
    view_bat._note.show()
  elif not notify_:
    view_bat._note.close()

  fmts = ["%{{A:bat:}}"]
  if bat_cap is not None:
    fmts.append("%{{T3}}{cap}%%{{T-}}")
  fmts.append("%{{T7}}%{{F{color}}}{sym}%{{F-}}%{{T-}}")
  if stat_sym is not None:
    fmts.append("%{{T4}}{stat_sym}%{{T-}}")
  fmts.append("%{{A}}")

  print(("bat=" + " ".join(fmts)).format(
      cap=bat_cap,
      color=color,
      sym=chars.EMSP + bat_sym(bat_cap),
      stat_sym=stat_sym
      ))

  view_bat._last_notify = notify_
