"""
Extensions to the built-in asyncio module
"""

import asyncio
import codecs

from asyncio import *

__all__ = list(asyncio.__all__) + [
  "DecodingStreamReader",
  "EncodingStreamReader",
  "read_pipe",
  "run_async"
  ]

class DecodingStreamReader:
  """A stream reader that automatically decodes what is read"""
  def __init__(self, reader, encoding="utf-8", errors="strict"):
    self.decoder = codecs.getincrementaldecoder(encoding)(errors)
    self.reader = reader

  async def __aiter__(self):
    return self

  async def __anext__(self):
    line = await self.readline()
    if line:
      return line
    raise StopAsyncIteration

  async def readline(self):
    return self.decoder.decode(await self.reader.readline())

  def at_eof(self):
    return self.reader.at_eof()

class EncodingStreamWriter:
  """A stream writer that automatically encodes what is written"""
  def __init__(self, writer, encoding="utf-8", errors="strict"):
    self.encoder = codecs.getincrementalencoder(encoding)(errors)
    self.writer = writer

  def close(self):
    self.writer.close()

  async def drain(self):
    await self.writer.drain()

  def write(self, data):
    self.writer.write(self.encoder.encode(data))

async def read_pipe(pipe, loop=None):
  """Get a reader that reads text from a pipe asynchronously."""
  reader = StreamReader(loop=loop)
  proto = StreamReaderProtocol(reader)
  await loop.connect_read_pipe(lambda: proto, pipe)
  return DecodingStreamReader(reader)

class _RunAsyncContextManager:
  def __init__(self, args, kwargs):
    self._coroutine = create_subprocess_exec(*args, **kwargs)

  async def __aenter__(self):
    self._proc = await self._coroutine
    stdin = EncodingStreamWriter(self._proc.stdin)
    stdout = DecodingStreamReader(self._proc.stdout)
    return stdin, stdout

  async def __aexit__(self, *exc_info):
    await self._proc.wait()

def run_async(*args, **kwargs):
  """Run a command in asynchronous context, yielding stdin and stdout."""
  return _RunAsyncContextManager(args, kwargs)
