"""
Configuration for herbstluftwm state information
"""

from .. import data
from .. import view
from ..lib import lemonbar

from . import colors

__all__ = []

TAG_STATE_FORMATS = {
  ".": "%{{F{c.herbst_tag_empty}}}{name}%{{F-}}", # Empty
  ":": "{name}", # Not empty
  "#": "%{{+u}}{name}%{{-u}}", # Focused
  "!": "{name}" # Urgent
  }

def format_tag(state, name):
  """Format a tag according to its state."""
  return TAG_STATE_FORMATS[state].format(
    c=colors,
    name=lemonbar.bar_escape(name)
    )

@data.transformer(keys=["tags"])
@data.on_val()
def transform_to_list(v):
  """Transform a tab-separated string into a list."""
  return v.split("\t")

@view.viewer
def view_tags(tags=[], **ds):
  """View the tags on the bar."""
  print("tags=" + " ".join(format_tag(t[0], t[1:]) for t in tags if t))

@view.viewer
def view_title(title=None, **ds):
  """View the title of the focused window on the bar."""
  print("title=%{{T2}}{title}%{{T-}}".format(
      title=lemonbar.bar_escape(title)
      ))