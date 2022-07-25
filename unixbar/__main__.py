"""
The entry point
"""

import collections
import concurrent
import contextlib
import io
import sys

from . import asynciox as asyncio
from . import config
from . import data
from . import lib
from . import subprocessx as subprocess
from . import threadingx as threading
from . import util
from . import view
from . import worker

@view.viewer
def view_quit(quit=None, **ds):
  """Allow workers to quit by sending quit data."""
  amain.done_future.set_result(None)

async def data_view_loop(data_, out_stream, drain_cb=None, loop=None,
  **kwargs):
  """Run viewers as needed when data changes."""
  views = util.DirtyDict()

  while True:
    await data_.dirty_future(loop=loop)
    # Yield to combine updates.
    await asyncio.sleep(0)

    with data_.dirtykeys() as dirty_keys:
      view_stream = io.StringIO()
      with threading.redirect_thread_stdout(view_stream):
        view.run_viewers(dirty_keys, collections.ChainMap(data_, kwargs))
      view_stream.seek(0)

      store = util.key_val_store(views)
      for line in view_stream:
        store(*util.key_val_split(line))

    if views.isdirty():
      with threading.redirect_thread_stdout(out_stream):
        config.print_bar(**collections.ChainMap(views, kwargs))
      views.clean()

      if drain_cb:
        await drain_cb()

async def amain(loop=None):
  """Run the bar asynchronously until a worker quits or something fails."""
  amain.done_future = loop.create_future()

  with contextlib.ExitStack() as s:
    s.enter_context(threading.thread_local_stdout())

    data_workers = worker.find_workers(lib.__path__)
    data_in, data_out = s.enter_context(
      util.open_pipe(rmode="rb", wbuffering=1)
      )

    # This pipe is a placeholder for worker communication.  It isn't used, but
    # it has to be open so workers can use blocking read to sleep.
    worker_in, worker_out = s.enter_context(util.open_pipe())
    with threading.redirect_thread_stdout(data_out):
      kwargs = s.enter_context(
        worker.run_workers(data_workers, worker_in=worker_in)
        )

    async with asyncio.run_async(
      *config.bar_args(),
      stdin=subprocess.PIPE,
      stdout=subprocess.PIPE
      ) as (bar_stdin, bar_stdout):
      data_reader = await asyncio.read_pipe(data_in, loop=loop)
      data_ = util.DirtyDict()

      data_read_coroutine = util.key_val_read_loop(
        data_reader,
        util.key_val_transform(
          util.key_val_store(data_),
          data.transformers()
          )
        )
      data_view_coroutine = data_view_loop(
        data_,
        util.Tee(bar_stdin, sys.stderr),
        drain_cb=bar_stdin.drain,
        loop=loop,
        **kwargs
        )

      click_coroutine = util.key_val_read_loop(
        bar_stdout,
        config.bar_click
        )

      _, pending = await asyncio.wait(
        [
          amain.done_future,
          data_read_coroutine,
          data_view_coroutine,
          click_coroutine
          ],
        return_when=concurrent.futures.FIRST_COMPLETED
        )
      for future in pending:
        future.cancel()

      bar_stdin.close()

def main():
  """Run the bar."""
  loop = asyncio.new_event_loop()
  loop.run_until_complete(amain(loop=loop))
  loop.close()

main()
