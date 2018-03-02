"""
This subpackage contains utility programs that can be called from
configuration code.
"""

import os

def environ():
  """Create a copy of the environment with this directory added to PATH."""
  path = list(filter(None, os.environ.get("PATH", "").split(":")))
  return dict(os.environ, PATH=":".join(__path__ + path))
