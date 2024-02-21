#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 16:47:42 2024

@author: kate
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
# Function for computing density
# empirical 'Nafe–Drake' relationship vp->rho Eqn1.  Brocher 2005 
# valid from 1500 m/s to 8500 m/s
def vp2rho(pvel):
    # check if your velocities are in bounds of the parameterization
    if np.min(pvel)<1.5:
        print("Proceed with caution lowest Vp is outside of parameterization")
    if np.max(pvel)>8.5:
        print("Proceed with caution highest Vp is outside of parameterization")

    # use equation
    rho=1.6612*pvel-0.4721*pvel**2+0.0671*pvel**3-0.0043*pvel**4+0.000106*pvel**5
    # #convert from g/cc to kg/m**3
    # rho=rho*1000
    rho=np.round(rho,2) #round to 2 decimal places
    return rho

# Some general setting stuff
name='MaunaKea'
suffix='.ppmod'
filename=name+suffix
delta=0.25

# Now we read in data and make it one dataframe
vr=pd.read_csv('out.vr_release', delim_whitespace=True,header=None, names=['lon','lat','depth','vp/vs'])
vmod=pd.read_csv('out.vp_release', delim_whitespace=True,header=None, names=['lon','lat','depth','vp'])
vs=np.round(vmod['vp']/vr['vp/vs'],2) # compute vs and round 
vmod.insert(4,'vs',vs)

# # Convert from km/s to m/s only if using cartesian coords
# vmod['vp']=vmod['vp']*1e3
# vmod['vs']=vmod['vs']*1e3

# Figure out how many lats, lons, and depths for header

lon_min=np.min(vmod['lon'])
lon_max=np.max(vmod['lon'])
lat_min=np.min(vmod['lat'])
lat_max=np.max(vmod['lat'])
depth_min=np.min(vmod['depth'])
depth_max=np.max(vmod['depth'])
Nlat=int(len(vmod['lat'].unique()))
Ndepth=int(len(vmod['depth'].unique()))
# for reasons I can't explain it was having trouble figuring out how many unique longitude
Nlon=int(len(vmod['lon'])/Nlat/Ndepth) 

# Vectors for lat and longitude variations
lon_vec=np.round(np.linspace(lon_min,lon_max, Nlon),4)
lat_vec=np.round(np.linspace(lat_min,lat_max, Nlat),4)
depth_vec= vmod['depth'].unique()
index_vec= np.arange(1, Ndepth+1, dtype=int)

# THIS SECTION COMPUTES THE DENSITY
vs_min=np.min(vmod['vs'])
vs_max=np.max(vmod['vs'])
vp_min=np.min(vmod['vp'])
vp_max=np.max(vmod['vp'])

rho=vp2rho(vmod['vp'])
rho_min=np.min(rho)
rho_max=np.max(rho)

# add rho to dataframe
vmod.insert(5,'rho',rho)

## open the textfile from before in append mode
file=open(filename,'w')

## Write Header
file.write(name+'\n'+
    str(delta)+'\n'+
    str(Nlat)+' '+str(lat_min)+' '+str(lat_max)+'\n'+
    str(Nlon)+' '+str(lon_min)+' '+str(lon_max)+'\n'+
    str(Ndepth)+' '+str(depth_min)+' '+str(depth_max)+'\n'+
    '-99 -99 -99 -99\n'+
    '.FALSE.\n')
file.close()

## Write depth profiles
# note the sorting looks weird because comparing floats in weird sometimes

for lat in lat_vec:
    lat_subset=vmod.loc[np.abs(vmod['lat']-lat)<1e-3,['lon','depth', 'vp','vs','rho']]
    for lon in lon_vec:
        depthprof=lat_subset.loc[np.abs(lat_subset['lon']-lon)<1e-2,['depth', 'vp','vs','rho']]
        depthprof.insert(0,'ind',index_vec)
        file=open(filename,'a')
        file.write(str(lat)+' '+str(lon)+' '+str(Ndepth)+'\n')
        file.close()
        depthprof.to_csv(filename, sep=' ', header=False, index=False, mode='a')


        