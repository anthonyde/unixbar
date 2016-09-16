"""
Configuration for WiFi status information and OSD
"""

import os

from .. import data
from .. import util
from .. import view
from ..lib import lemonbar

__all__ = []

os.environ["WIFI_DEV"] = "wlp3s0"

# Wifi symbols (i3fonticon)
WIFI_OFF = "\uec5c"
WIFI_ZERO = "\uec5d"
WIFI_LOW = "\uea26"
WIFI_MED = "\uea27"
WIFI_HIGH = "\uea28"

# Wifi quality states
WIFI_QUAL_ZERO = 15
WIFI_QUAL_LOW = 40
WIFI_QUAL_MED = 70

# Signal dBm quality range
WIFI_DBM_MIN = -100
WIFI_DBM_MAX = -50

def wifi_qual(dbm):
  """Convert dBm to quality (percent)."""
  if dbm is None:
    return None
  elif dbm <= WIFI_DBM_MIN:
    return 0
  elif dbm >= WIFI_DBM_MAX:
    return 100
  else:
    return 2 * (dbm + 100)

def wifi_qual_bin(qual):
  """Bin quality values such that wifi_sym(qual_bin) = wifi_sym(qual)."""
  if qual is None:
    return None
  for bin_ in (WIFI_QUAL_MED, WIFI_QUAL_LOW, WIFI_QUAL_LOW):
    if qual > bin_:
      return bin_
  return 0

def wifi_sym(qual, osd=False):
  """Return the symbol for a quality."""
  if qual is None:
    if osd:
      return WIFI_OFF
    else:
      return WIFI_ZERO
  elif qual < WIFI_QUAL_ZERO:
    return WIFI_ZERO
  elif qual < WIFI_QUAL_LOW:
    return WIFI_LOW
  elif qual < WIFI_QUAL_MED:
    return WIFI_MED
  else:
    return WIFI_HIGH

@data.transformer(keys=["wifi_dbm"])
@data.on_val(key="wifi_qual")
def transform_to_qual(v):
  """Transform signal dBm to quality."""
  try:
    dbm = int(v)
  except ValueError:
    dbm = None
  return wifi_qual_bin(wifi_qual(dbm))

@view.viewer
def view_wifi(wifi_qual=None, wifi_ssid=None, **ds):
  """View WiFi status on the bar."""
  fmts = []
  if wifi_ssid is not None:
    fmts.append("{ssid}")
  fmts.append("{sym}")
  print(("wifi=%{{A:wifi:}}" + " ".join(fmts) + "%{{A}}").format(
      sym=wifi_sym(wifi_qual),
      ssid=lemonbar.bar_escape(wifi_ssid)
      ))

@view.viewer
@util.staticvars(_first=True)
def view_wifi_osd(osd_out, wifi_ssid=None, **ds):
  """View an OSD on WiFi status changes."""
  if not view_wifi_osd._first:
    wifi_qual = ds.get("wifi_qual", None)
    print("%{{c}}{sym}\n%{{c}}{ssid}".format(
        sym=wifi_sym(wifi_qual, osd=True),
        ssid=lemonbar.bar_escape(wifi_ssid) if wifi_ssid is not None else ""
        ), file=osd_out)

  view_wifi_osd._first = False
