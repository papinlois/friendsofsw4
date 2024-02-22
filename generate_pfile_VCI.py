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
name='VancouverIsland'
suffix='.ppmod'
filename=name+suffix
delta=0.25

# Now we read in data and make it one dataframe
# vr=pd.read_csv('out.vr_release', delim_whitespace=True,header=None, names=['lon','lat','depth','vp/vs'])
vmod=pd.read_csv('Savard_VpVs.txt', delim_whitespace=True,header=None, names=['lon', 'lat', 'depth', 'vp', 'vs', 'DWS'])
# vs=np.round(vmod['vp']/vr['vp/vs'],2) # compute vs and round 
# vmod.insert(4,'vs',vs)

plt.plot(vmod['lon'],vmod['lat'],'ko')

# this is a chunk that grids the velocity model
from scipy.interpolate import griddata
latmin=47
latmax=51
lonmin=-126
lonmax=-121
lats=np.round(10*np.arange(latmin,latmax,0.1))/10
lons=np.round(10*np.arange(lonmin,lonmax,0.1))/10
depths= [0.,  3.,  6.,  9., 12., 15., 18., 21., 24., 27., 30., 33., 36.,
       39., 42., 45., 48., 51., 54., 57., 60., 63., 66., 69., 72., 75.,
       78., 81., 84., 87., 90., 93.]
grid=np.zeros((len(lats)*len(lons)*len(depths),3))
ii = 0
for lon in lons:
    for lat in lats:
        for dep in depths:
            grid[ii,0], grid[ii,1], grid[ii,2]=lon, lat, dep
            ii+=1
        
grid_vp = griddata((vmod['lon'],vmod['lat'],vmod['depth']), vmod['vp'], 
                    (grid), method='linear')
grid_vs = griddata((vmod['lon'],vmod['lat'],vmod['depth']), vmod['vs'], 
                    (grid), method='linear')
vmod_interp = pd.DataFrame(np.hstack((grid,
                                      grid_vp.reshape(len(lats)*len(lons)*len(depths),1),
                                      grid_vs.reshape(len(lats)*len(lons)*len(depths),1))), 
                           columns=['lon', 'lat', 'depth', 'vp', 'vs'])


plt.figure()
d=3
dslice=vmod[vmod['depth']==d]
dslice_interp=vmod_interp[vmod_interp['depth']==d]
plt.scatter(dslice['lon'],dslice['lat'],20,dslice['vp'],vmin=4,vmax=7)
plt.scatter(dslice_interp['lon'],dslice_interp['lat'],20,dslice_interp['vp'],edgecolors='black',vmin=4,vmax=7)

# Check for NAN drama
assert np.isnan(vmod_interp['vp']).sum() == 0 and np.isnan(vmod_interp['vs']).sum() == 0

vmod_interp['rho']=vp2rho(vmod_interp['vp'])

'''
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
lon_vec=vmod.loc[vmod['depth']==depth_min].loc[vmod['lat']==lat_min]['lon'].to_numpy()
lat_vec=vmod['lat'].unique()
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
'''
## open the textfile from before in append mode
file=open(filename,'w')

## Write Header
# f'whatever str {this is a var:.3f}'
file.write(name+'\n'+
    str(delta)+'\n'+
    str(len(lats))+' '+str(np.min(lats))+' '+f"{np.max(lats):.1f}"+'\n'+
    str(len(lons))+' '+str(np.min(lons))+' '+f"{np.max(lons):.1f}"+'\n'+
    str(len(depths))+' '+str(np.min(depths))+' '+str(np.max(depths))+'\n'+
    '-99 -99 -99 -99\n'+
    '.FALSE.\n')
file.close()

## Write depth profiles
# note the sorting looks weird because comparing floats in weird sometimes

Ndepth=len(depths)
for lat in lats:
    for lon in lons:
        print(lat, lon, Ndepth)
        tmp=vmod_interp[(vmod_interp['lat']==lat) & (vmod_interp['lon']==lon)]
        tmp.insert(0,'ind',range(1,len(depths)+1))
        print(tmp[['ind','depth','vp','rho']])
        # depthprof=lat_subset.loc[np.abs(lat_subset['lon']-lon)<1e-2,['depth', 'vp','vs','rho']]
        file=open(filename,'a')
        file.write(str(lat)+' '+str(lon)+' '+str(Ndepth)+'\n')
        file.close()
        tmp[['ind','depth','vp','rho']].to_csv(filename, sep=' ', header=False, index=False, mode='a')
