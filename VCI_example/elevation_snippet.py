#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 27 14:49:06 2024

Download .nc topo file for some region of interest

@author: amt
"""
import xarray as xr
import pygmt

minlon, maxlon, minlat, maxlat = -125, -122, 47, 49

reg=[minlon-0.02, maxlon+0.02, minlat-0.02, maxlat+0.02]
grid = pygmt.datasets.load_earth_relief(resolution='03s', region=reg) # this gets the dataset. region is [minlon, maxlon, minlat, maxlat]
grid.to_netcdf('svi_topo_03s.nc')