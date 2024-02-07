import pygmt
import xarray as xr

maxlon=-154.713
minlon=-156.14
minlat=18.9
maxlat=20.28
reg=[minlon-0.02, maxlon+0.02, minlat-0.02, maxlat+0.02]
grid = pygmt.datasets.load_earth_relief(resolution='03s', region=reg) # this gets the dataset. region is [minlon, maxlon, minlat, maxlat]
grid.to_netcdf('maunakea_topo_03s.nc')
f = '/Users/kate/Documents/DLPs/SW4/TopographyModel/maunakea_topo_03s.nc'
grid = xr.open_dataset(f)
lon = grid['lon'].to_numpy()
lat = grid['lat'].to_numpy()
elev = grid['elevation'].to_numpy()
