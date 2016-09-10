"""
Tools for finding and running viewers that format data for presentation
"""

import collections
import inspect

from . import util

# decorator
@util.staticvars(_viewers=collections.defaultdict(set))
def viewer(f):
  """A decorator for registering a viewer using its arguments as data keys"""
  for arg in inspect.getargspec(f).args:
    viewer._viewers[arg].add(f)
  return f

def run_viewers(dirty_keys, d):
  """Run viewers listening on dirty data."""
  dirty_viewers = set()
  for k in dirty_keys:
    dirty_viewers.update(viewer._viewers.get(k, set()))
  for v in dirty_viewers:
    v(**d)
