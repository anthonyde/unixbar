"""
Clock configuration
"""

import datetime

from .. import data
from .. import view

__all__ = []

@data.transformer(keys=["timestamp"])
@data.on_val()
def transform_timestamp(v):
  """Return a timestamp with minute precision to avoid unnecessary updates."""
  d = datetime.datetime.fromtimestamp(float(v))
  secs = datetime.timedelta(seconds=d.second, microseconds=d.microsecond)
  return d - secs

@view.viewer
def view_clock(timestamp, **ds):
  """View the date and time on the bar."""
  print("clock=" + timestamp.strftime("%a %-d %b %-H:%M"))
