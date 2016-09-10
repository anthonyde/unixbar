"""
A library for interfacing with lemonbar
"""

from .. import config
from .. import util

@util.compose(lambda argss: [arg for args in list(argss) for arg in args])
def bar_args(bar, geometry=None, fonts=(), name=None,
  underline=None, bg=None, fg=None):
  """Return a lemonbar command with arguments from keyword arguments."""
  yield bar,
  if geometry is not None:
    geometry = [g if g is not None else "" for g in geometry]
    yield "-g", "{}x{}+{}+{}".format(*geometry)
  for font in fonts:
    yield "-f", font
  if name is not None:
    yield "-n", name
  if underline is not None:
    yield "-u", str(underline)
  if bg is not None:
    yield "-B", bg
  if fg is not None:
    yield "-F", fg

def bar_escape(s):
  """Escape arbitrary text to make it safe for rendering."""
  return s.replace("\n", "^J").replace("%{", "%" + config.BAR_ZWSP + "{")
