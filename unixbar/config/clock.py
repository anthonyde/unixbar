"""
Clock configuration
"""

import datetime

from .. import view

__all__ = []

@view.viewer
def view_clock(timestamp, **ds):
  """View the date and time on the bar."""
  print("clock=" + str(datetime.datetime.fromtimestamp(float(timestamp))))
