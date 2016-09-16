"""
Configuration for an audio status icon and OSD
"""

from .. import data
from .. import view

from . import chars
from . import util

__all__ = []

# Volume symbols (i3fonticon)
AUDIO_MUTE = "\uea42" + chars.MULT
AUDIO_LOW = "\uea42"
AUDIO_MED = "\uea43"
AUDIO_HIGH = "\uea44"

# Volume states
AUDIO_VOL_LOW = 54
AUDIO_VOL_MED = 69

AUDIO_N_MAX = 16

def audio_n(vol):
  """Map ALSA volume [0, 74] onto [0, 16]."""
  return int((10 ** (vol / 63) - 1) * 8 / 7 + 1 / 2)

def audio_sym(on, vol, osd=False):
  """Get the symbol for an audio state."""
  if not on:
    return AUDIO_MUTE
  elif osd:
    return AUDIO_HIGH
  elif vol < AUDIO_VOL_LOW:
    return AUDIO_LOW
  elif vol < AUDIO_VOL_MED:
    return AUDIO_MED
  else:
    return AUDIO_HIGH

@data.transformer(keys=["audio_on"])
@data.on_val()
def transform_to_bool(v):
  """Transform "on"/other -> True/False."""
  return "on" == v

@data.transformer(keys=["audio_vol"])
@data.on_val()
def transform_to_int(v):
  """Transform a string to an int."""
  return int(v)

@view.viewer
@util.staticvars(_first=True)
def view_audio(osd_out, audio_on=None, audio_vol=None, **ds):
  """View the audio status on the bar and changes in an OSD."""
  if not view_audio._first:
    print("%{{c}}{sym}\n%{{c}}%{{T2}}{vol_bar}%{{T-}}".format(
        sym=audio_sym(audio_on, audio_vol, osd=True),
        vol_bar=util.prog_bar(audio_n(audio_vol), AUDIO_N_MAX)
        ),
      file=osd_out
      )
  print("audio=%{{A:audio:}}%{{T4}}{sym}%{{T-}}%{{A}}".format(
      sym=audio_sym(audio_on, audio_vol)
      ))

  view_audio._first = False
