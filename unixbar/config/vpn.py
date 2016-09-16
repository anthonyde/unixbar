"""
Configuration for a VPN status icon
"""

import os

from .. import data
from .. import view

__all__ = []

os.environ["VPN_FIFO"] = "/var/run/vpn-virtual-up.fifo"

VPN_UP = "\ue8a1" # i3fonticon

@data.transformer(keys=["vpn_up"])
@data.on_val()
def transform_to_bool(v):
  """Transform "y"/other -> True/False."""
  return "y" == v

@view.viewer
def view_vpn(vpn_up=False, **ds):
  """View the VPN status on the bar."""
  print("vpn=" + VPN_UP * vpn_up)
