"""
Configuration for a VPN status icon
"""

import os

from .. import data
from .. import view

__all__ = []

os.environ["VPN_FIFO"] = "/var/run/vpn-virtual-up.fifo"

VPN_UP = "\ue9c9" # IcoMoon-Free

@data.transformer(keys=["vpn_up"])
@data.on_val()
def transform_to_bool(v):
  """Transform "y"/other -> True/False."""
  return "y" == v

@view.viewer
def view_vpn(vpn_up=False, **ds):
  """View the VPN status on the bar."""
  if vpn_up:
    print("vpn=%{{T6}}{sym}%{{T-}}".format(sym=VPN_UP))
  else:
    print("vpn=")
