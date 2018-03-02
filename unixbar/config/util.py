"""
Miscellaneous configuration things that don't fit anywhere else
"""

import math

from . import chars

from ..util import *

__all__ = []

def log_scale(x, y):
  """Calculate a value k such that x * log(10) = k * log(y + 1)."""
  return x * math.log(10) / math.log(y + 1)

def exp_transform(k, x):
  """Map a value x onto an exponential curve defined by k."""
  return 10 ** (x / k) - 1

def log_transform(k, y):
  """Map a value y onto a logarithmic curve defined by k."""
  return k * math.log(y + 1) / math.log(10)

def nonempty_keys(d):
  """Get a set of non-empty keys in a dict."""
  return set(k for k, v in d.items() if v is not "")

def prog_bar(n, nmax):
  """Generate a progress bar string representing n of nmax."""
  return chars.HRSP.join([chars.BFUL] * n + [chars.B8TH] * (nmax - n))
