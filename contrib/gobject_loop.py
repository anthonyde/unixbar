"""
A worker that processes GObject messages
"""

import gi
from gi.repository import GObject

from .. import worker

@worker.threadworker
def gobject_loop(**kwargs):
  """Run the GObject main loop."""
  GObject.MainLoop().run()
