"""
Color configuration that is automatically loaded from xrdb
"""

import re

from .. import subprocessx as subprocess

__all__ = []

XRDB_COLOR_PATTERN = re.compile(
  r"\*(background|foreground|color(?:\d|1[0-5])):\s+#([\dA-Fa-f]+)\n")

def load_colors():
  with subprocess.check_stdout_text(["xrdb", "-query"]) as lines:
    for line in lines:
      if XRDB_COLOR_PATTERN.fullmatch(line):
        exec(XRDB_COLOR_PATTERN.sub(r"\1='#ff\2'", line), globals())

load_colors()
