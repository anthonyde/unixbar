"""
The config subpackage contains modules that set up workers and viewers.

By default all names exported from config modules are exposed at the package
level to make them available to workers and library code regardless of where
they are defined in the hierarchy.

Code in this subpackage is meant to be modified by users and the default
import behavior can be changed or removed if desired (e.g. to require all
exposed names to be defined in a specific package or to use a single-file
configuration.)
"""

from ..util import import_submodules as _import_submodules

def _import_all(module):
  try:
    all_ = module.__all__
  except AttributeError:
    all_ = (name for name in module.__dict__ if not name.startswith("_"))
  globals().update({name: getattr(module, name) for name in all_})

_import_submodules(__path__, prefix=__name__ + ".", module_cb=_import_all)
