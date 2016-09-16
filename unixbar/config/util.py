"""
Miscellaneous configuration things that don't fit anywhere else
"""

from . import chars

from ..util import *

__all__ = []

def nonempty_keys(d):
  """Get a set of non-empty keys in a dict."""
  return set(k for k, v in d.items() if v is not "")

def prog_bar(n, nmax):
  """Generate a progress bar string representing n of nmax."""
  return chars.HRSP.join([chars.BFUL] * n + [chars.B8TH] * (nmax - n))
