"""
Extensions to the built-in subprocess module
"""

import contextlib
import subprocess

from subprocess import *

__all__ = subprocess.__all__ + [
  "check_output_text",
  "check_stdin",
  "check_stdin_text",
  "check_stdout",
  "check_stdout_text",
  "run_async"
  ]

@contextlib.contextmanager
def run_async(*args, check=False, **kwargs):
  """Run a command in context, yielding stdin and stdout."""
  with Popen(*args, **kwargs) as proc:
    yield proc.stdin, proc.stdout
  retcode = proc.poll()
  if check and retcode:
    raise CalledProcessError(retcode, proc.args, None, None)

@contextlib.contextmanager
def check_stdin(*args, **kwargs):
  """Run a command, yielding stdin and checking for success."""
  with run_async(*args, stdin=PIPE, check=True, **kwargs) as ios:
    stdin, _ = ios
    yield stdin

def check_stdin_text(*args, **kwargs):
  """Run a command, yielding text-based stdin and checking for success."""
  return check_stdin(*args, bufsize=1, universal_newlines=True, **kwargs)

@contextlib.contextmanager
def check_stdout(*args, **kwargs):
  """Run a command, yielding stdout and checking for success."""
  with run_async(*args, stdout=PIPE, check=True, **kwargs) as (_, stdout):
    yield stdout

def check_stdout_text(*args, **kwargs):
  """Run a command, yielding text-based stdout and checking for success."""
  return check_stdout(*args, bufsize=1, universal_newlines=True, **kwargs)

def check_output_text(*args, **kwargs):
  """Run a command, yielding its output text and checking for success."""
  return check_output(*args, universal_newlines=True, **kwargs)
