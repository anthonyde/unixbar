"""
A worker that displays content on a multi-panel OSD
"""

import contextlib
import itertools
import select
import types

from .. import config
from .. import subprocessx as subprocess
from .. import util
from .. import worker

@worker.initkwargs
def osd_init():
  """Open a pipe for transmitting OSD content."""
  with util.open_pipe(buffering=1) as (osd_in, osd_out):
    util.restrict_write(osd_out.buffer, select.PIPE_BUF)
    yield dict(
      osd_in=osd_in,
      osd_out=osd_out
      )

def osd_write(self, s):
  """Write newline-delimited OSD content to multiple streams."""
  parts = s.split("\n")
  while parts:
    self._stdin.write(parts.pop(0))
    if parts:
      self._stdin.write("\n")
      self._stdin = next(self._stdin_iter)

def osd_input(argss):
  """Create a stream-like object that displays written text on OSD panels."""
  with contextlib.ExitStack() as s:
    stdins = []
    for args in argss:
      stdin_context = subprocess.check_stdin_text(args)
      stdins.append(s.enter_context(stdin_context))

    # Lazy class
    self = s.pop_all()
    self._stdin_iter = itertools.cycle(stdins)
    self._stdin = next(self._stdin_iter)
    self.write = types.MethodType(osd_write, self)
    return self

@worker.threadworker
def osd_worker(osd_in, **kwargs):
  """Display the OSD when content is received."""
  poll = select.poll()
  poll.register(osd_in.fileno(), select.POLLIN)
  while True:
    if not poll.poll():
      continue
    argss = config.osd_argss()
    with osd_input(argss) as osd_stdin:
      while True:
        for _ in argss: # To copy the correct number of lines
          # XXX This throws ValueError: I/O operation on closed file on quit.
          print(osd_in.readline(), end="", file=osd_stdin)
        if not poll.poll(config.OSD_DELAY_MS):
          break
