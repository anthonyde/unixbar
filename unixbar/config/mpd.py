"""
Configuration for an MPD status icon
"""

import os

from .. import data
from .. import view

__all__ = []

os.environ["MPD_HOST"] = "mpd"

MPD_PLAY = "\uea15" # IcoMoon-Free

@data.transformer(keys=["mpd_stat"])
@data.on_val(key="mpd_play")
def transform_to_bool(v):
  """Transform "playing"/other -> True/False."""
  return "playing" == v

@view.viewer
def view_mpd(mpd_play=False, **ds):
  """View MPD status on the bar."""
  if mpd_play:
    print("mpd=%{{A:mpd:}}%{{T6}}{sym}%{{T-}}%{{A}}".format(sym=MPD_PLAY))
  else:
    print("mpd=")
