"""
A worker that publishes on/off blink data (e.g. for blinking symbols)
"""

import time
import weakref

from .. import config
from .. import util
from .. import worker

@worker.initkwargs
def blink_init():
  """Initialize the means to request blink data."""
  yield dict(
    blink_listeners=util.make_waitable_set(weakref.WeakSet())
    )

@worker.threadworker
def blink_worker(blink_listeners, **kwargs):
  """Blink if anyone is listening."""
  blink = False
  while True:
    blink_listeners.clear_event()
    if blink_listeners:
      print("blink={blink}".format(blink=int(blink)))
      time.sleep(config.BLINK_INTERVAL_S)
      blink = not blink
    else:
      blink_listeners.wait()
