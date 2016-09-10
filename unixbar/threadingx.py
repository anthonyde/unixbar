"""
Extensions to the built-in threading module
"""

import contextlib
import sys
import threading
import weakref

from threading import *

__all__ = threading.__all__ + [
  "InheritableThreadLocal",
  "ThreadLocalStreamProxy",
  "redirect_thread_stdout",
  "redirect_thread_stream",
  "thread_local_stdout"
  ]

class InheritableThreadLocal(local):
  """Thread-local storage that can be inherited by new threads"""
  _instances = weakref.WeakSet()

  def __init__(self):
    self._instances.add(self)

  @classmethod
  def load_all(cls):
    """Copy the active thread's storage for transferring to a new thread."""
    return {tls: tls.__dict__.copy() for tls in cls._instances}

  @classmethod
  def store_all(cls, loaded):
    """Commit copied storage to the active thread."""
    for tls, d in loaded.items():
      tls.__dict__.update(d)

class ThreadLocalStreamProxy:
  """A stream-like proxy that supports thread-local overrides"""
  def __init__(self, original_stream):
    self._tls = InheritableThreadLocal()
    self._tls.stream = original_stream

  @property
  def stream(self):
    return self._tls.stream

  @stream.setter
  def stream(self, new_target):
    self._tls.stream = new_target

  def __getattr__(self, name):
    return getattr(self.stream, name)

@contextlib.contextmanager
def redirect_thread_stream(stream_proxy, new_target):
  """Redirect a stream for this thread and its inheritors."""
  if not isinstance(stream_proxy, ThreadLocalStreamProxy):
    raise ValueError("stream_proxy is not ThreadLocalStreamProxy")

  old_stream = stream_proxy.stream
  stream_proxy.stream = new_target
  try:
    yield
  finally:
    stream_proxy.stream = old_stream

class thread_local_stdout(contextlib.redirect_stdout):
  """A stdout redirector that enables thread-local overrides"""
  def __init__(self):
    super().__init__(ThreadLocalStreamProxy(sys.stdout))

def redirect_thread_stdout(new_target):
  """Redirect stdout for this thread and its inheritors."""
  return redirect_thread_stream(sys.stdout, new_target)
