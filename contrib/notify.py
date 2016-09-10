"""
A library for sending desktop notifications with GLib
"""

import gi
gi.require_version("Notify", "0.7")
from gi.repository import Notify

from .. import config
from .. import util
from .. import worker
from ..lib import gobject_loop # For connect

class Note:
  """A high-level notification"""
  def __init__(self, summary="", body=""):
    self._note = Notify.Notification.new(summary, body)
    self._note.set_urgency(Notify.Urgency.CRITICAL)
    self._note.connect("closed", self._on_close)
    self._dirty = True
    self._visible = False

  def _on_dirty(self):
    self._dirty = True

  def _on_close(self, note):
    self._visible = False

  @util.dirtyproperty(_on_dirty)
  def summary(self):
    return self._note.props

  @util.dirtyproperty(_on_dirty)
  def body(self):
    return self._note.props

  def update(self):
    """Update the text if needed."""
    if self._dirty and self._visible:
      self.show()

  def show(self):
    """Ensure that the notification is visible and up to date."""
    self._note.show()
    self._visible = True
    self._dirty = False

  def close(self):
    """Hide the note."""
    self._note.close()

@worker.initkwargs
def notify_init():
  """Initialize the notification system."""
  Notify.init(config.NOTIFY_APP_NAME)
  try:
    yield {}
  finally:
    Notify.uninit()
