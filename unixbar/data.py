"""
Tools for transforming data
"""

from . import util

@util.staticvars(_dict={})
def transformers():
  """Get the registered transformers."""
  return transformers._dict

def register_transformer(keys, f):
  """Register a transformer for the given keys."""
  for k in keys:
    transformers._dict[k] = f

# decorator
def transformer(keys=[]):
  """A decorator that registers a function as a transformer"""
  def decorate(f):
    register_transformer(keys, f)
  return decorate

# decorator
def on_val(key=None):
  """A decorator that converts a transformer from value to key-value."""
  def decorate(f):
    if key is None:
      return lambda k, v: [(k, f(v))]
    else:
      return lambda _, v: [(key, f(v))]
  return decorate
