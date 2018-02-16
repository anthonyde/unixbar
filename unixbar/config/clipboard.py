"""
Configuration for a clipboard status icon
"""

from .. import data
from .. import view

__all__ = []

CLIP_DATA = "\ue8de" # i3fonticon

@data.transformer(keys=["clip_data"])
@data.on_val()
def transform_to_bool(v):
  """Transform non-zero/zero -> True/False."""
  return bool(int(v))

@view.viewer
def view_clip(clip_data=False, **ds):
  """View the clipboard status on the bar."""
  if clip_data:
    print("clip=%{{A:clip:}}{sym}%{{A}}".format(sym=CLIP_DATA))
  else:
    print("clip=")
