"""
Bar configuration
"""

__all__ = [
  "bar_args",
  "bar_click",
  "print_bar"
  ]

def bar_args():
  """Return the bar command with arguments."""
  return ["lemonbar", "-B", "#ff000000", "-F", "#ffffff00"]

def bar_click(k, v):
  """Do something when the bar is clicked."""
  pass

def print_bar(**views):
  """Print the bar contents."""
  print("%{{r}}{v[clock]}".format(v=views))
