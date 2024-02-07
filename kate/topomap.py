#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 16:29:11 2024

@author: kate
"""
import pygmt
maxlon=-154.713
minlon=-156.14
minlat=18.9
maxlat=20.28
reg=[minlon, maxlon, minlat, maxlat]
grid = pygmt.datasets.load_earth_relief(resolution='03s', region=reg)
fig = pygmt.Figure()

fig.grdimage(
    grid=grid,
    cmap="haxby",
    projection="M15c",
    frame=True,
)
fig.grdcontour(grid=grid, interval=500, annotation=1000)
fig.colorbar(frame=["a1000", "x+lElevation", "y+lm"])
fig.show()
