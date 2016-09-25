"""
Tools for finding and running workers that generate data
"""

import contextlib
import os
import signal
import subprocess
import sys

from . import threadingx as threading
from . import util

class ThreadWorker:
  """A thread-based worker"""
  def __init__(self, worker_fn):
    self._worker_fn = worker_fn

  @contextlib.contextmanager
  def start(self, **kwargs):
    """Start the worker, inheriting any thread locals."""
    threading.Thread(
      target=self._run_thread_worker,
      kwargs=dict(
        _loaded_tls=threading.InheritableThreadLocal.load_all(),
        **kwargs
        ),
      daemon=True
      ).start()
    yield

  def _run_thread_worker(self, _loaded_tls=None, **kwargs):
    threading.InheritableThreadLocal.store_all(_loaded_tls)
    util.rename_proc(self._worker_fn.__name__)
    return self._worker_fn(**kwargs)

# decorator
@util.staticvars(_workers=[])
def threadworker(f):
  """A decorator for registering a function as a thread worker"""
  threadworker._workers.append(ThreadWorker(f))
  return f

class ProcessWorker:
  """A process-based worker"""
  def __init__(self, path):
    self._path = path

  @contextlib.contextmanager
  def start(self, worker_in=None, **kwargs):
    """Start the worker, terminating it and its children on exit."""
    proc = subprocess.Popen(
      self._path,
      stdin=worker_in,
      stdout=sys.stdout, # Use redirected sys.stdout
      preexec_fn=os.setsid
      )
    try:
      yield
    finally:
      if proc.stdout:
        proc.stdout.close()
      if proc.stderr:
        proc.stderr.close()
      try: # Flushing a BufferedWriter may raise an error.
        if proc.stdin:
          proc.stdin.close()
      finally:
        # terminate() will leave running child processes.
        os.killpg(os.getpgid(proc.pid), signal.SIGTERM)

def executable_workers(path):
  """Find all executable workers on a path."""
  for dir in path:
    for entry in os.scandir(dir):
      if entry.is_file() and os.access(entry.path, os.X_OK):
        yield ProcessWorker(entry.path)

def find_workers(path):
  """Find all thread- and process-based (on a path) workers."""
  return threadworker._workers + list(executable_workers(path))

# decorator
@util.staticvars(_fns=[])
def initkwargs(f):
  """A decorator for initializing shared worker resources"""
  cm = contextlib.contextmanager(f)
  initkwargs._fns.append(cm)
  return cm

@contextlib.contextmanager
def run_workers(workers, **kwargs):
  """Initialize resources, run workers, and clean up on exit."""
  with contextlib.ExitStack() as s:
    for f in initkwargs._fns:
      kwargs.update(s.enter_context(f()))

    for worker in workers:
      s.enter_context(worker.start(**kwargs))

    yield kwargs
