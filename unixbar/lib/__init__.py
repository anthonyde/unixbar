"""
This subpackage is a library of components that are loaded with the status
bar.  These components can include Python modules that define workers or
expose functions for use by configuration or other components as well as
standalone executables that will be run as worker processes.

To use components from a shared library, symlink them here.
"""

from .. import util

util.import_submodules(__path__, prefix=__name__ + ".")
