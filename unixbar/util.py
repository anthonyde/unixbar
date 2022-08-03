"""
Miscellaneous things that don't fit anywhere else
"""

import collections
import contextlib
import ctypes
import os
import pkgutil
import threading
import types
import warnings

__all__ = [
  "DirtyDict",
  "Tee",
  "compose",
  "dirtyproperty",
  "import_submodules",
  "key_val_split",
  "key_val_store",
  "key_val_transform",
  "key_val_read_loop",
  "make_waitable_set",
  "open_pipe",
  "rename_proc",
  "restrict_write",
  "staticvars"
  ]

_libc = ctypes.cdll.LoadLibrary("libc.so.6")

class DirtyDict(dict, collections.abc.MutableMapping):
  """A dictionary that can signal updates"""
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self._dirty = set()
    self._dirty_futures = []

  def __delitem__(self, key):
    super().__delitem__(key)
    self._dirty.add(key)
    self._set_futures()

  def __setitem__(self, key, value):
    if self._diff_value(key, value):
      super().__setitem__(key, value)
      self._dirty.add(key)
      self._set_futures()

  def _diff_value(self, key, newvalue):
    try:
      return self[key] != newvalue
    except KeyError:
      return True

  def _set_futures(self):
    if self.isdirty():
      for future in self._dirty_futures:
        future.set_result(None)
      self._dirty_futures.clear()

  def dirty_future(self, loop=None):
    """Get a future for the next update."""
    dirty_future = loop.create_future()
    self._dirty_futures.append(dirty_future)
    return dirty_future

  def isdirty(self):
    """Whether an update was made since the last clean"""
    return bool(self._dirty)

  def clean(self):
    """Acknowledge all past updates."""
    self._dirty.clear()

  @contextlib.contextmanager
  def dirtykeys(self):
    """Get any updated keys, acknowledging the updates on exit."""
    yield self._dirty
    self.clean()

class _DirtyProperty:
  def __init__(self, fdata, attr, fdirty):
    self._fdata = fdata
    self._attr = attr
    self._fdirty = fdirty

  def __get__(self, obj):
    return getattr(self._fdata(obj), self._attr)

  def __set__(self, obj, value):
    data = self._fdata(obj)
    if getattr(data, self._attr) != value:
      setattr(data, self._attr, value)
      self._fdirty(obj)

# decorator
def dirtyproperty(fdirty):
  """A decorator for creating an attribute wrapper that tracks dirtiness"""
  def decorate(f):
    return _DirtyProperty(f, f.__name__, fdirty)
  return decorate

# decorator
def compose(g):
  """A decorator for function composition (useful with generators.)"""
  def decorate(f):
    return lambda *args, **kwargs: g(f(*args, **kwargs))
  return decorate

class Tee:
  """A stream-like helper for writing to multiple streams"""
  def __init__(self, *streams):
    self._streams = streams

  def write(self, data):
    """Write data to all component streams."""
    for stream in self._streams:
      stream.write(data)

def import_submodules(path, prefix=None, module_cb=None):
  """Load submodules on a path, optionally calling back with each module."""
  for finder, name, ispkg in pkgutil.walk_packages(path, prefix=prefix):
    if name == "__main__":
      continue
    module = finder.find_module(name).load_module(name)
    if module_cb:
      module_cb(module)

def key_val_split(line):
  r"""Split a string of the form key '=' [value] '\n' into a pair."""
  parts = line.rstrip("\n").split("=", 1)
  k = parts.pop(0)
  v = parts.pop(0) if parts else None
  return k, v

def key_val_store(out_dict):
  """Make a key-value handler that stores into a dict."""
  def f(k, v):
    if v is not None:
      out_dict[k] = v
    else:
      try:
        del out_dict[k]
      except KeyError:
        pass
  return f

def _transform_identity(k, v):
  yield k, v

def key_val_transform(handler, transformers):
  """Extend a key-value handler by running transformers."""
  def f(k, v):
    for k, v in transformers.get(k, _transform_identity)(k, v):
      handler(k, v)
  return f

async def key_val_read_loop(reader, handler):
  """Read key-value strings from a reader and pass them to a handler."""
  async for line in reader:
    # The inside of this loop must be atomic (no await) to prevent data from
    # being read but not handled when execution is cancelled.
    handler(*key_val_split(line))

def make_waitable_set(s):
  """Extend a set to support waiting for additions."""
  event = threading.Event()

  old_add = s.add
  def add(self, value):
    old_add(value)
    event.set()
  s.add = types.MethodType(add, s)

  def clear_event(self):
    event.clear()
  s.clear_event = types.MethodType(clear_event, s)

  def wait(self, timeout=None):
    return event.wait(timeout)
  s.wait = types.MethodType(wait, s)

  return s

@contextlib.contextmanager
def open_pipe(rmode="r", wmode="w", buffering=-1, rbuffering=None,
  wbuffering=None):
  """Create and open a pipe."""
  if rbuffering is None:
    rbuffering = buffering
  if wbuffering is None:
    wbuffering = buffering

  rfd, wfd = os.pipe()
  with open(rfd, mode=rmode, buffering=rbuffering) as rstream, \
    open(wfd, mode=wmode, buffering=wbuffering) as wstream:
    yield rstream, wstream

def rename_proc(name):
  """Rename the active process (only on Linux.)"""
  name_bytes = name.encode()
  buf = ctypes.create_string_buffer(len(name_bytes) + 1)
  buf.value = name_bytes
  _libc.prctl(15, ctypes.byref(buf), 0, 0, 0)

def restrict_write(buf, max_len):
  """Restrict the length of writes to a buffer."""
  old_write = buf.write
  def write(self, b):
    if len(b) > max_len:
      warnings.warn("write exceeds maximum length; dropping", RuntimeWarning)
      return
    old_write(b)
  buf.write = types.MethodType(write, buf)

# decorator
def staticvars(**kwargs):
  """A decorator for initializing variables defined on a function"""
  def decorate(f):
    for k, v in kwargs.items():
      setattr(f, k, v)
    return f
  return decorate
