"""
A worker that periodically publishes timestamps
"""

import time

from .. import worker

@worker.threadworker
def time_worker(**kwargs):
  """Publish timestamp data."""
  while True:
    print("timestamp=" + str(time.time()))
    time.sleep(1)
