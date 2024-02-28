#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 24 11:00:00 2024

Convert netcdf (.nc) files to the topo format required for SW4

@author: kate
"""
import xarray as xr
import pandas as pd
import numpy as np

file2load='svi_topo_03s.nc'
# Specify the file path where you want to save the CSV file
file_path = 'svi_topo_03s.topo'

# read topo from netcdf
grid = xr.open_dataset(file2load)

# sort by lat and lon
df_grid = grid.to_dataframe().reset_index().sort_values(['lat', 'lon'])
                     
# add nb lon nb lat as first line
custom_first_line = f"{len(grid.lon.data)} {len(grid.lat.data)}"

# Open the file in write mode and add the custom first line
with open(file_path, 'w') as file:
    file.write(custom_first_line + '\n')

# Append the DataFrame to the CSV file
df_grid.to_csv(file_path, mode='a', index=False, header=False, float_format='%.3f', sep=' ')